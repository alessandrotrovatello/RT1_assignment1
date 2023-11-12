from __future__ import print_function

import time
from sr.robot import *

"""
Assignment 1 python script

It is requested to write a python node that controls the robot to put all the golden tokens togheter.

My personal implementation has the following steps:
	- 1) count how many tokens there are in the arena and put their IDs in a list.
	- 2) set as reference token the first token saw and save its ID.
	- 3) search the unpaired token and grab it.
	- 4) find the reference token.
	- 5) release the unpaired token near to reference token.
	- 6) repeat 3-5 steps until there are no more unpaired tokens.

To read better what the robot does, I added a simple delay between actions to avoid annoying motion messages.
I could reduce the speeds and seconds of drive() and turn() functions but the robot would be too slow.
One of the task of the assignment doesn't include the time to reach the goal, but i preferred to speed up the robot.
	
"""
a_th = 5.0
""" float: Threshold for the control of the orientation """

d_th = 0.4
""" float: Threshold for the control of the linear distance """

R = Robot()
""" instance of the class Robot """

p_th = 2
""" int: Threshold for release the unpaired token to the reference token  """

delay = 7
""" int: delay time to read better what the robot do. """

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args:
		speed (int): the speed of the wheels
		seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args:
		speed (int): the speed of the wheels
		seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
				
def rotation(rot_y):
	"""
	Function to adjust the robot's orientation relative to the token
        
	Args: 
		rot_y (float): rotation about the Y axis in degrees
	Returns:
		rot_y (float): rotation about the Y axis in degrees
	"""
	if -a_th <= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
		print("Ah, here we are!")
		drive(40, 0.05)
	elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left
		print("Left a bit...")
		turn(-10, 0.05)
	elif rot_y > a_th: # if the robot is not well aligned with the token, we move it on the right
		print("Right a bit...")
		turn(+10, 0.05)
		
	return rot_y # updated rotation

def count_token():
	"""
	Function to count how many tokens there are in arena and save their IDs in a list.
	The first token seen it will be the reference token.
	
	Returns:
		id_list (list): list of token IDs
		reference_id (int): ID of the reference token
	"""
	id_list = []
	dist=100
	i=0
	for i in range(12): # The Robot goes around 360 degrees
		print("I'm scanning the arena.")
		for token in R.see():
			if token.info.code not in id_list: # Saves all the IDs of the tokens seen in a list only if the ID is not already present within the list
				id_list.append(token.info.code)
		turn(20,0.5)	
		
	n = len(id_list) # Numbers of tokens in the arena
	print("There are",n,"tokens in the arena and their IDs are:",id_list)
	
	reference_id = id_list[0] # Set the first seen as the reference token
	print("The reference token ID is:",reference_id)
	
	id_list.remove(reference_id) # Remove the reference token ID from the id_list
	m = len(id_list) # Numbers of unpaired tokens
	print("The unpaired tokens are",m,"and their IDs are:", id_list)
	
	return id_list, reference_id # Return the id_list of unpaired token and the ID of reference token

	
def find_unpaired_token(id_list, reference_id):
	"""
	Function to find unpaired token.
	
	Args:
		id_list (list): list of token IDs
		reference_id (int): ID of the reference token
	
	Return:
		id_list (list): list of token IDs
	"""
	dist=100
	while True:
		for token in R.see():
			if token.info.code != reference_id and token.info.code in id_list and token.dist < dist: # Looks for the token with the ID different from the reference ID
																									 # and that it is within the id_list and within the robot's vision radius
				dist = token.dist
				rot_y = token.rot_y
		if dist==100 or dist==-1:
			print("I don't see unpaired token!")
			turn(-50,0.05);
		elif dist < d_th: 
			print("Unpaired token found!")
			if R.grab(): # if we are close to the token, we grab it.
				print("I got the token with ID:",token.info.code)
				time.sleep(delay)
				
				find_reference_token(reference_id) # Find the reference token to release near it the token just got
				
				id_list.remove(token.info.code) # Remove from unpareid token IDs list the token ID just paired
				print("I removed from id_list the token with ID:",token.info.code)
				print("The new list is:",id_list)
				print("Other", len(id_list),"tokens to pair.")
				time.sleep(delay)
			else:
				print("I'm not close enough");
		elif -a_th <= rot_y <= a_th or rot_y < -a_th or rot_y > a_th:
			rot_y = rotation(rot_y) # Adjust the orientation of the robot relative to the unpaired token
			
		return id_list # Return the updated id_list
	return 1
	
def find_reference_token(reference_id):
	"""
	Function to find the reference token.
	
	Args:
		reference_id (int): reference token ID
	"""
	dist=100
	while True:
		for token in R.see():
			if token.info.code is reference_id:# and token.dist < dist:
				dist = token.dist
				rot_y = token.rot_y
		if dist==100 or dist==-1:
			print("I don't see the reference token!!")
			turn(-50,0.05);
		elif dist < 2*d_th: 
			print("Reference token found!")
			if R.release(): # if we are close to the token, we release it.
				print("Token paired!");
				drive(-30,1)
				turn(30,2)
				break
		elif -a_th <= rot_y <= a_th or rot_y < -a_th or rot_y > a_th:
			rot_y = rotation(rot_y) # Adjust the orientation of the robot relative to the reference token
	return 1
		
def main():
	id_list, reference_id = count_token() # The robot scans the area around it to count how many tokens are in the arena and set the reference token ID
	time.sleep(delay)
	while id_list: # Until the id_list of unpaired tokens is empty
		id_list = find_unpaired_token(id_list, reference_id) # Find unpaired token and took it to reference token
	print("There are no more unpaired tokens!")
		
main()


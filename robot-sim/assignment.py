from __future__ import print_function

import time
from sr.robot import *

"""
Assignment 1 python script

It is requested to write a python node that controls the robot to put all the golden tokens togheter.

The code have the following steps:
	- 1) counts how many tokens there are in arena and put the ID of each token in a list
	- 2) find the nearest token and save its ID
	- 3) put each unpaired token to nearest token found
	
"""
a_th = 5.0
""" float: Threshold for the control of the orientation"""

d_th = 0.4
""" float: Threshold for the control of the linear distance"""

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
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
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0
				
def rotation(rot_y):
	"""
	Function to adjust the robot's direction with respect to the token
        
	Args: rot_y (float): rotation about the Y axis in degrees
	"""
	if -a_th <= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
		print("Ah, here we are!.")
		print(type(rot_y))
		drive(50, 0.05)
	elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left
		print("Left a bit...")
		turn(-10, 0.05)
	elif rot_y > a_th: # if the robot is not well aligned with the token, we move it on the right
		print("Right a bit...")
		turn(+10, 0.05)
	return rot_y

def count_token():
	"""
	Function to count how many tokens there are in arena and save their ID in a list.
	
	Returns:
	n (int): numbers of tokens
	id_list (list): list of token ids
	"""
	id_list = []
	dist=100
	primo = True
	for i in range(12):
		#if primo:
		#	for token in R.see():
		#		if token.dist < dist:
		#			first_id = token.info.code
		#			primo = False
		for token in R.see():
			if token.info.code not in id_list:
				id_list.append(token.info.code)
		turn(20,0.5)
	#id_list.remove(first_id)
	first_id = id_list[0]
	id_list.remove(first_id)
	n = len(id_list)
	return n, id_list, first_id

	
def find_token(id_list, first_id):
	dist=100
	while True:
		for token in R.see():
			if token.info.code != first_id and token.info.code in id_list:# and token.dist < dist:
				dist = token.dist
				rot_y = token.rot_y
				token_id = token.info.code
		if dist==100:
			print("I don't see any token!!")
			turn(50,0.05);
		elif dist < d_th: 
			print("Token Found!")
			if R.grab(): # if we are close to the token, we grab it.
				print("Gotcha!",token.info.code)
				find_first(first_id,id_list)
				id_list.remove(token.info.code)
				print("I removed from id_list the token with id:",token.info.code)
				print("The new list is:",id_list)
				print("Other", len(id_list),"token to pair")
			else:
				print("I'm not close enough");
		elif -a_th <= rot_y <= a_th or rot_y < -a_th or rot_y > a_th:
			rot_y = rotation(rot_y)
		return id_list
	
def find_first(first_id,id_list):
	dist=100
	while True:
		for token in R.see():
			if token.info.code is first_id:# and token.dist < dist:
				dist = token.dist
				rot_y = token.rot_y
		if dist==100:
			print("I don't see any token!!")
			turn(50,0.05);
		elif dist < 2*d_th: 
			print("Token Found!")
			if R.release(): # if we are close to the token, we release it.
				drive(-30,1)
				turn(30,2)
				break
		elif -a_th <= rot_y <= a_th or rot_y < -a_th or rot_y > a_th:
			rot_y = rotation(rot_y)

def main():
	n, id_list, first_id = count_token()
	print("There are", n,"tokens and their id are:", id_list)
	#print("The first token i see is:",first_id)	
	while id_list:
		id_list = find_token(id_list, first_id)
	print("There is no more unpaired token!")
		

main()


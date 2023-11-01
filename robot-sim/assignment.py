from __future__ import print_function

import time
from sr.robot import *

"""
Assignment 1 python script

It is requested to write a python node that controls the robot to put all the goledn boxes togheter.

The code have the following steps:
	- 1) counts how many tokens there are in arena and put the id of each token in a list
	- 2) find the nearest token and grab it
	- 3) put each unpaired token to first token grabbed
	
"""
a_th = 2.0
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
		

def count_token():
	"""
	Function to count how many tokens there are in arena and save their ID in a set.
	
	Returns:
	n (int): numbers of tokens
	id_set (set): set of token id
	"""
	id_set = []
	dist=100
	for i in range(12):
		for token in R.see():
			token_id = token.info.code
			if token_id not in id_set and token_id:
				id_set.append(token_id)
		turn(10,1)
	first_id = max(id_set)
	id_set.remove(first_id)
	n = len(id_set)
	return n, id_set, first_id

	
def find_token(id_set, first_id):
	dist=100
	while True:
		for token in R.see():
			if token.info.code is not first_id and token.info.code in id_set:
				dist = token.dist
				rot_y = token.rot_y
				id_token = token.info.code
		if dist==100:
			print("I don't see any token!!")
			turn(-10,1);
		elif dist < d_th: 
			print("Token Found!")
			if R.grab(): # if we are close to the token, we grab it.
				print("Gotcha!")
				#turn(30,2)
				#R.release()
				#turn(-30,2)
				#drive(30,1)
				print(token.info.code)
				id_set.remove(token.info.code)
				print("I removed from id_set list the token with id:",id_token)
				print("The new list is:",id_set)
				print("Other", len(id_set),"token to pair")
				find_first(first_id)
				print("Ho appena finito di eseguire find_first",id_set)
			else:
				print("I'm not close enough");
		elif -a_th <= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
			print("Ah, here we are!.",id_token)
			drive(100, 0.01)
		elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			print("Left a bit...")
			turn(-2, 0.5)
		elif rot_y > a_th:
			print("Right a bit...")
			turn(+2, 0.5)
		return id_set
		
def find_first(first_id):
	dist=100
	while True:
		for token in R.see():
			if token.info.code is first_id:
				dist = token.dist
				rot_y = token.rot_y
		if dist==100:
			print("I don't see any token!!")
			turn(-10,1);
		elif dist < 1.8*d_th: 
			print("Token Found!")
			R.release() # if we are close to the token, we grab it.
			drive(-30,1)
			turn(30,2)
			break
		elif -a_th <= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
			print("Ah, here we are!.",token.info.code)
			drive(100, 0.01)
		elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			print("Left a bit...")
			turn(-2, 0.5)
		elif rot_y > a_th:
			print("Right a bit...")
			turn(+2, 0.5)

def main():
	#n, id_set, first_id = count_token()
	n, id_set, first_id = count_token()
	print("There are", n,"tokens and their id are:", id_set)
	#print("The first token i see is:",first_id)
	while id_set:
		id_set = find_token(id_set, first_id)
	print("There is no more unpaired token!")
		

main()


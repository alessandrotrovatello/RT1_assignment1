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

def find_first_token():
    """
    Function to find the closest token

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
	rot_y (float): angle between the robot and the token (-1 if no token is detected)
    """
    dist=100
    for token in R.see():
        if token.dist < dist:
        	dist = token.dist
        	rot_y = token.rot_y
    if dist==100:
		return -1, -1
    else:
   		return dist, rot_y
   	
def main():
	while 1:
		dist, rot_y = find_first_token()
		if dist==-1:
			print("I don't see any token!!")
			turn(+10,1);
		elif dist < d_th: 
			print("Token Found!")
			if R.grab(): # if we are close to the token, we grab it.
				print("Gotcha!")
			else:
				print("I'm not close enough");
		elif -a_th <= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
			print("Ah, here we are!.")
			drive(10, 0.5)
		elif rot_y < -a_th: # if the robot is not well aligned with the token, we move it on the left or on the right
			print("Left a bit...")
			turn(-2, 0.5)
		elif rot_y > a_th:
			print("Right a bit...")
			turn(+2, 0.5)		

main()


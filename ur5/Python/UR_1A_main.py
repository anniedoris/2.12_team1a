from UR5 import *
import time
import readchar
from readchar import key
import keyboard
from key_definitions import *
import math

"""
This is the main file for running the UR5 motion control. It enables a user to run the UR5
from a keyboard on which this script is running. It allows for:

- coordinate control (in cylindrical coordiantes)
- speed control (three different speed options)
- A6 (last joint) control
- motion to three pre-defined house positions 
- motion to certain pre-defined z heights

This file references the UR5 class (see UR5.py) frequently.
Definition of the different keys used can be found in key_definitions.py.

"""

# Robot initialization
robot = UR5("169.254.157.0")
print("Robot initialized")

# Stores information about what key was last pressed in case we reach joint limits
last_key_pressed = None

# Helper function for printing angles in degrees
def print_degrees(l):
    deg_l = []
    for i in l:
        deg_l.append(i * (180.0/math.pi))
    return deg_l

# Continuous main loop
while True:

    # Checks to see if we are approaching limits on any of the joints
    # limitCheck() returns True if the check passed, false if it does not
    if robot.limitCheck():
        # set all key flags to true, no joint issues, all keys are enabled
        theta_pos_key_enabled = True
        theta_neg_key_enabled = True
        radius_pos_key_enabled = True
        radius_neg_key_enabled = True
        z_pos_key_enabled = True
        z_neg_key_enabled = True
        a6_neg_key_enabled = True
        a6_pos_key_enabled = True
        
    # Disable the key that was just pressed that caused the limitCheck() to fail
    else:
        if last_key_pressed == THETA_POS_KEY:
            theta_pos_key_enabled = False
        elif last_key_pressed == THETA_NEG_KEY:
            theta_neg_key_enabled = False
        elif last_key_pressed == RADIUS_POS_KEY:
            radius_pos_key_enabled = False
        elif last_key_pressed == RADIUS_NEG_KEY:
            radius_neg_key_enabled = False
        elif last_key_pressed == Z_NEG_KEY:
            z_neg_key_enabled = False
        elif last_key_pressed == Z_POS_KEY:
            z_pos_key_enabled = False
        elif last_key_pressed == A6_NEG_KEY:
            a6_neg_key_enabled = False
        elif last_key_pressed == A6_POS_KEY:
            a6_pos_key_enabled = False
        print(f"{last_key_pressed} KEY IS DISTABLED BECAUSE OF JOINT LIMITS")

    # Get the robot's current position, so we can move based on where the robot is
    robot.get_current_robot_info()
    
    # Print out the robot's current z height to give the operator more information
    print("Robot pose z height: ")
    print(robot.current_global_pose[2])

    # List of flags for whether keys are enabled or not. If all the values in this list are True,
    # then all keys are enabled (no joint limit issues)
    all_keys_enabled = [theta_pos_key_enabled, theta_neg_key_enabled, radius_pos_key_enabled, radius_neg_key_enabled, z_pos_key_enabled, z_neg_key_enabled, a6_neg_key_enabled, a6_pos_key_enabled]

    # All the following if/elif statements check to see what key is pressed by the user to
    # perform the corresponding action
    if keyboard.is_pressed(LOW_SPEED_KEY) and all(all_keys_enabled):
        robot.move_velocity = 0.01 # update robot velocity to low speed

    elif keyboard.is_pressed(MED_SPEED_KEY) and all(all_keys_enabled):
        robot.move_velocity = 0.1 # update robot velocity to medium speed

    elif keyboard.is_pressed(HIGH_SPEED_KEY) and all(all_keys_enabled):
        robot.move_velocity = 0.2 # update robot velocity to high speed
    
    elif keyboard.is_pressed(HIGH_Z_KEY) and all(all_keys_enabled):
        robot.send_to_z_height('up')

    elif keyboard.is_pressed(LOW_Z_KEY) and all(all_keys_enabled):
        robot.send_to_z_height('down')

    elif keyboard.is_pressed(LEFT_HOME_KEY) and all(all_keys_enabled):
        robot.send_to_house_location('left')

    elif keyboard.is_pressed(MIDDLE_HOME_KEY) and all(all_keys_enabled):
        robot.send_to_house_location('middle')

    elif keyboard.is_pressed(RIGHT_HOME_KEY) and all(all_keys_enabled):
        robot.send_to_house_location('right')

    elif keyboard.is_pressed(THETA_POS_KEY) and theta_pos_key_enabled:
        robot.vel_cylindrical('theta', 'pos')
        last_key_pressed = THETA_POS_KEY

    elif keyboard.is_pressed(THETA_NEG_KEY) and theta_neg_key_enabled:
        robot.vel_cylindrical('theta', 'neg')
        last_key_pressed = THETA_NEG_KEY

    elif keyboard.is_pressed(RADIUS_NEG_KEY) and radius_pos_key_enabled:
        robot.vel_cylindrical('radius', 'neg')
        last_key_pressed = RADIUS_NEG_KEY

    elif keyboard.is_pressed(RADIUS_POS_KEY) and radius_neg_key_enabled:
        robot.vel_cylindrical('radius', 'pos')
        last_key_pressed = RADIUS_POS_KEY

    elif keyboard.is_pressed(Z_NEG_KEY) and z_neg_key_enabled:
        robot.vel_cylindrical('z', 'neg')
        last_key_pressed = Z_NEG_KEY

    elif keyboard.is_pressed(Z_POS_KEY) and z_pos_key_enabled:
        robot.vel_cylindrical('z', 'pos')
        last_key_pressed = Z_POS_KEY

    elif keyboard.is_pressed(A6_POS_KEY) and a6_pos_key_enabled:
        robot.rotate_a6('pos')
        last_key_pressed = A6_POS_KEY

    elif keyboard.is_pressed(A6_NEG_KEY) and a6_neg_key_enabled:
        robot.rotate_a6('neg')
        last_key_pressed = A6_NEG_KEY
        
    else:
        robot.zero_velocity()
        
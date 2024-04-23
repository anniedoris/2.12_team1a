from UR5 import *
import time
import readchar
from readchar import key
import keyboard
from key_definitions import *
import math

robot = UR5("169.254.157.0")
print("Robot initialized")
last_key_pressed = None

def print_degrees(l):
    deg_l = []
    for i in l:
        deg_l.append(i * (180.0/math.pi))
    return deg_l

while True:

    if robot.limitCheck():
        theta_pos_key_enabled = True
        theta_neg_key_enabled = True
        radius_pos_key_enabled = True
        radius_neg_key_enabled = True
        z_pos_key_enabled = True
        z_neg_key_enabled = True
        a6_neg_key_enabled = True
        a6_pos_key_enabled = True
    else:
        if last_key_pressed == THETA_POS_KEY:
            theta_pos_key_enabled = False
        elif last_key_pressed == THETA_NEG_KEY:
            theta_neg_key_enabled = False
        elif last_key_pressed == RADIUS_POS_KEY:
            radius_pos_key_enabled = False
        elif last_key_pressed == RADIUS_NEG_KEY:\
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

    robot.get_current_robot_info()
    print("Robot pose: ")
    print(robot.current_global_pose)
    print("Robot cylindrical coords: ")
    print(robot.current_polar)
    print("Robot joint coords: ")
    print(print_degrees(robot.current_joint_values))

    all_keys_enabled = [theta_pos_key_enabled, theta_neg_key_enabled, radius_pos_key_enabled, radius_neg_key_enabled, z_pos_key_enabled, z_neg_key_enabled, a6_neg_key_enabled, a6_pos_key_enabled]

    if keyboard.is_pressed('1') and all(all_keys_enabled):
        robot.move_velocity = 0.01
    
    elif keyboard.is_pressed('2') and all(all_keys_enabled):
        robot.move_velocity = 0.1

    elif keyboard.is_pressed('3') and all(all_keys_enabled):
        robot.move_velocity = 0.2

    elif keyboard.is_pressed(THETA_POS_KEY) and theta_pos_key_enabled:
        robot.vel_polar('theta', 'pos')
        last_key_pressed = THETA_POS_KEY

    elif keyboard.is_pressed(THETA_NEG_KEY) and theta_neg_key_enabled:
        robot.vel_polar('theta', 'neg')
        last_key_pressed = THETA_NEG_KEY

    elif keyboard.is_pressed(RADIUS_NEG_KEY) and radius_pos_key_enabled:
        robot.vel_polar('radius', 'neg')
        last_key_pressed = RADIUS_NEG_KEY

    elif keyboard.is_pressed(RADIUS_POS_KEY) and radius_neg_key_enabled:
        robot.vel_polar('radius', 'pos')
        last_key_pressed = RADIUS_POS_KEY

    elif keyboard.is_pressed(Z_NEG_KEY) and z_neg_key_enabled:
        robot.vel_polar('z', 'neg')
        last_key_pressed = Z_NEG_KEY

    elif keyboard.is_pressed(Z_POS_KEY) and z_pos_key_enabled:
        robot.vel_polar('z', 'pos')
        last_key_pressed = Z_POS_KEY

    elif keyboard.is_pressed(A6_POS_KEY) and a6_pos_key_enabled:
        # robot.vel_polar('z', 'pos')
        # robot.vel_joint('a6', 'pos')
        # TODO: figure out how to add A6 control
        print("A6 +")
        last_key_pressed = A6_POS_KEY

    elif keyboard.is_pressed(A6_NEG_KEY) and a6_neg_key_enabled:
        # robot.vel_polar('z', 'pos')
        # robot.vel_joint('a6', 'neg')
        # TODO: figure out ho to add A6 control
        print("A6 -")
        last_key_pressed = A6_NEG_KEY
        
    else:
        robot.zero_velocity()
'''
while True:

    robot.get_current_robot_info()

    if keyboard.is_pressed('1'):
        robot.move_velocity = 0.01
    
    elif keyboard.is_pressed('2'):
        robot.move_velocity = 0.1

    elif keyboard.is_pressed('3'):
        robot.move_velocity = 0.2

    elif keyboard.is_pressed('left'):
        robot.vel_cart('x', 'pos')

    elif keyboard.is_pressed('right'):
        robot.vel_cart('x', 'neg')

    elif keyboard.is_pressed('down'):
        robot.vel_cart('y', 'pos')

    elif keyboard.is_pressed('up'):
        robot.vel_cart('y', 'neg')

    elif keyboard.is_pressed('a'):
        robot.vel_cart('z', 'neg')

    elif keyboard.is_pressed('q'):
        robot.vel_cart('z', 'pos')
        
    else:
        robot.zero_velocity()
        print("no key pressed")
'''
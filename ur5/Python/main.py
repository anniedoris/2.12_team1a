from UR5 import *
import time
import readchar
from readchar import key
import keyboard

robot = UR5("169.254.157.0")
print("Robot initialized")

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

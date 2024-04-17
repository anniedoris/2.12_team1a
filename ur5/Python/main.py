from UR5 import *
import time
import readchar
from readchar import key

robot = UR5("169.254.157.0")
print("Robot initialized")

while True:

    robot.get_current_robot_info()
    
    inp = readchar.readkey()

    if inp == key.UP:
        robot.move_cart('x', 'pos')

    if inp == key.DOWN:
        robot.move_cart('x', 'neg')

    if inp == key.RIGHT:
        robot.move_cart('y', 'pos')
    
    if inp == key.LEFT:
        robot.move_cart('y', 'neg')

    if inp == 'q':
        robot.move_cart('z', 'pos')
    
    if inp == 'a':
        robot.move_cart('z', 'neg')

    time.sleep(0.003)
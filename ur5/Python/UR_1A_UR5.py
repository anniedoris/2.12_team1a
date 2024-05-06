
import rtde_control
import rtde_receive
import numpy as np
import math

"""
Defines the UR5 class which is used by main.py.
"""

class UR5:
    def __init__(self, ip_address):
        
        # Storing motion information
        self.move_velocity = 0.01 # Stores the velocity at which the robot will move
        self.move_acceleration = 6.0 # Stores the acceleration at whcih the robot will move
        self.current_polar = [0,0,0] # Current polar will be stored as r, theta, z
        self.current_global_pose = [0, 0, 0, 0, 0, 0] # TCP pose in the global coordinate frame
        self.current_x = self.current_global_pose[0] # Get x coordinate of TCP
        self.current_y = self.current_global_pose[1] # Get y coordiante of TCP
        self.current_z = self.current_global_pose[2] # Get z coordinate of TCP
        self.current_joint_values = [0, 0, 0, 0, 0, 0] # Storing current joint values
        
        # Control objects
        self.rtde_c = rtde_control.RTDEControlInterface(ip_address) # Object for control
        self.rtde_r = rtde_receive.RTDEReceiveInterface(ip_address) # Object for receiving
        
        # Information about joint limits
        self.joint_lower_limits = [-math.pi*2.0, -math.pi*2.0, -math.pi*2.0, -math.pi*2.0, -math.pi*2.0, -math.pi*2.0] # The lower limits for all joints is -360 deg
        self.joint_upper_limits = [math.pi*2.0, math.pi*2.0, math.pi*2.0, math.pi*2.0, math.pi*2.0, math.pi*2.0] # The upper limits for all joints is 360 deg
        self.buffer_limit = 0.1 # Limit in radians (0.1 rad is ~5.7 deg). So if joints are within 5.7 deg of limit, motion in the problematic direction will be disabled
        
        # Predefined house locations
        home_middle = [44.38, -65.62, 58.64, 6.8, 90.93, 0.2] # defines position of center house in robot joint coordinates
        home_right = [127, -65.62, 58.64, 6.8, 90.93, 0.2] # defines position of right house in robot joint coordinates
        home_left = [-45, -65.62, 58.64, 6.8, 90.93, 0.2] # defines position of left house in robot joint coordinates
        self.home_right = [(math.pi * i)/180.0 for i in home_right]
        self.home_left = [(math.pi * i)/180.0 for i in home_left]
        self.home_middle = [(math.pi * i)/180.0 for i in home_middle]
        
        # During initialization, send the robot to starting position, which is the center house
        self.rtde_c.moveJ(self.home_middle, 0.2, self.move_acceleration)

    def get_current_robot_info(self):
        '''
        Get the current robot position information.
        '''
        
        # Get current joint angles and end effector position
        self.current_joint_values = self.rtde_r.getActualQ()
        self.current_global_pose = self.rtde_r.getActualTCPPose()
        self.current_x = self.current_global_pose[0]
        self.current_y = self.current_global_pose[1]
        self.current_z = self.current_global_pose[2]
        
        # Update cylindrical coordinates
        self.current_polar[0] = np.sqrt(self.current_x**2+self.current_y**2) # get r value
        self.current_polar[1] = np.arctan2(self.current_y, self.current_x) # get theta value
        self.current_polar[2] = self.current_z # get z value, just use global z coordinate
        return
    
    def limitCheck(self):
        '''
        Checks to see if any of the joints are approaching the joint limits.
        
        Return: True if limit check passes, False if joints are approaching a limit.
        '''
        
        limit_list = [] # Will contain boolean for each joint, True if no limit issues, False if limit issues
        
        # Go through all current joint values
        for i, j in enumerate(self.current_joint_values):
            
            # If joint value within limits, add True to limit_list
            if (j < (self.joint_upper_limits[5] - self.buffer_limit)) and (j > (self.joint_lower_limits[i] + self.buffer_limit)):
                limit_list.append(True)
                
            # Otherwise add False
            else:
                limit_list.append(False)
        
        if all(limit_list):
            return True
        
        # If any Falses in limit_list, return False
        else:
            print("Stopping before singularity") # Give message to user
            return False

    def vel_cylindrical(self, coord, pos):
        '''
        This function moves the robot in cylindrical coordaintes, theta, r and z.
        Theta is relative to rotation around the robot base, z is height, and r is radially out from robot base.
        
        coord: can specify either `radius`, `theta`, or `z`
        pos: can specify either `pos` or `neg` for motion in one direction or the other
        '''
        
        # Stores the velocity vector we will ultimately send to the robot
        target_vel = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        
        # Move in the robot's radial direction (in and out from the base)
        if coord == 'radius':
            if pos == 'pos':
                target_vel[0] = self.move_velocity* np.cos(self.current_polar[1])
                target_vel[1] = self.move_velocity* np.sin(self.current_polar[1])
            
            else:
                target_vel[0] = -self.move_velocity* np.cos(self.current_polar[1])
                target_vel[1] = -self.move_velocity* np.sin(self.current_polar[1])
        
        # Move in the robot's theta direction (around base joint)
        elif coord == 'theta':
            if pos == 'pos':
                target_vel[0] = -self.move_velocity * np.sin(self.current_polar[1])
                target_vel[1] = self.move_velocity * np.cos(self.current_polar[1])
                target_vel[5] = self.move_velocity *np.pi/2 # This ensures that the end effector also rotates with radial rotation

            else:
                target_vel[0] = self.move_velocity * np.sin(self.current_polar[1])
                target_vel[1] = -self.move_velocity * np.cos(self.current_polar[1])
                target_vel[5] = -self.move_velocity *np.pi/2 # This ensures that the end effector also rotates with radial rotation
        
        # Move in the z direction 
        elif coord == 'z':
            if pos == 'pos':
                target_vel[2] = self.move_velocity
            else:
                target_vel[2] = -self.move_velocity
        
        # Send the new velocity vector to the robot
        self.rtde_c.jogStart(speeds = target_vel)
        return
    
    def send_to_house_location(self, house):
        '''
        This function moves the robot to pre-defined house locations.
        
        house: can specify either 'left', 'right', or 'middle'
        '''
        
        self.rtde_c.jogStop() # have to turn off jogging before we can use moveJ
        
        # Send to the left house
        if house == 'left':
            self.rtde_c.moveJ(self.home_left, 0.4, self.move_acceleration)
        
        # Send to the right house
        elif house == 'right':
            self.rtde_c.moveJ(self.home_right, 0.4, self.move_acceleration)
        
        # Send to the middle house
        elif house == 'middle':
            self.rtde_c.moveJ(self.home_middle, 0.4, self.move_acceleration)
        
        # Turn back on jogStart before leaving function so arrow keys work
        self.rtde_c.jogStart(speeds = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        return
    
    def send_to_z_height(self, down_or_up):
        '''
        This function moves the robot to a pre-defined z coordinate. All other coordinates remain unchanged.
        Just moves the robot up in z.
        
        down_or_up: can specify either 'down' or 'up'
        '''
        
        if down_or_up == 'up':
            new_height = self.current_global_pose
            new_height[2] = 0.65 # send the z coordinate to 650 mm
            self.rtde_c.jogStop() # turn off jog control to use moveL
            self.rtde_c.moveL(new_height,0.15,self.move_acceleration)
            self.rtde_c.jogStart(speeds = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]) # turn back on jog control
        else:
            new_height = self.current_global_pose
            new_height[2] = 0.1 # send the z coordinate to 100 mm
            self.rtde_c.jogStop() # turn off jog control to use moveL
            self.rtde_c.moveL(new_height,0.15,self.move_acceleration)
            self.rtde_c.jogStart(speeds = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]) # turn back on jog control
        return
            
    def rotate_a6(self, direciton):
        '''
        This function rotates the A6/last joint of the robot.
        
        direction: can specify either 'pos' or 'neg'
        '''
        
        # Stores the velocity vector we will ultimately send to the robot
        target_vel = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        
        if direciton == 'pos':
            target_vel[5] = self.move_velocity*5 # add factor of 5 to make motion faster, otherwise very slow
        else:
            target_vel[5] = -self.move_velocity*5
        
        # Send the new velocity vector to the robot
        self.rtde_c.jogStart(speeds = target_vel)
        return
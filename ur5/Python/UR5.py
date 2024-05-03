
import rtde_control
import rtde_receive
import numpy as np
import math

class UR5:
    def __init__(self, ip_address):
        self.current_global_pose = [0, 0, 0, 0, 0, 0] # Global coordinate system pose
        self.current_rotated_pose = [0, 0, 0, 0, 0, 0] # Coordinate system defined by rotation of the base joint
        self.current_joint_values = [0, 0, 0, 0, 0, 0] # Storing current joint values
        self.current_polar = [0,0,0] # Current polar will be stored as r, theta, z
        self.rtde_c = rtde_control.RTDEControlInterface(ip_address) # Object for control
        self.rtde_r = rtde_receive.RTDEReceiveInterface(ip_address) # Object for receiving
        self.current_x = self.current_global_pose[0]
        self.current_y = self.current_global_pose[1]
        self.current_z = self.current_global_pose[2]
        self.move_velocity = 0.01
        self.move_acceleration = 6.0
        self.default_move_dist = 0.01
        self.move_dist = 0.001 # This is a move distance in meters
        self.joint_lower_limits = [-math.pi*2.0, -math.pi*2.0, -math.pi*2.0, -math.pi*2.0, -math.pi*2.0, -math.pi*2.0]
        self.joint_upper_limits = [math.pi*2.0, math.pi*2.0, math.pi*2.0, math.pi*2.0, math.pi*2.0, math.pi*2.0]
        self.buffer_limit = 0.1 # radians buffer limit

        # Send the robot to a good initialized configuration
        # The most important part of this is being able to "square" the robot so the end effector is flat w.r.t the ground
        # TODO: Update to a pose that we are happy with for initialization
        self.rtde_c.moveL([-0.015, -0.55, 0.444, -0.001, 3.13, 0.001], 0.2, self.move_acceleration)

    def get_current_robot_info(self):
        self.current_joint_values = self.rtde_r.getActualQ()
        self.current_global_pose = self.rtde_r.getActualTCPPose()
        self.current_x = self.current_global_pose[0]
        self.current_y = self.current_global_pose[1]
        self.current_z = self.current_global_pose[2]
        
        self.current_polar[0] = np.sqrt(self.current_x**2+self.current_y**2) # get r value
        self.current_polar[1] = np.arctan2(self.current_y, self.current_x) # get theta value, just use A1 joint
        self.current_polar[2] = self.current_z # get z value, just use global z coordinate
        return

    def update_move_dist(self, new_move_dist):
        self.move_dist = new_move_dist
        return

    def vel_cart(self, coord, pos):
        target_vel = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

        if coord == 'x':
            if pos == 'pos':
                target_vel[0] = self.move_velocity
            else:
                target_vel[0] = -self.move_velocity

        elif coord == 'y':
            if pos == 'pos':
                target_vel[1] = self.move_velocity
            else:
                target_vel[1] = -self.move_velocity

        elif coord == 'z':
            if pos == 'pos':
                target_vel[2] = self.move_velocity
            else:
                target_vel[2] = -self.move_velocity

        self.rtde_c.jogStart(speeds = target_vel)
        return

    def vel_joint(self, coord, pos):
        target_joints = self.current_joint_values

        if coord == 'a6':
            if pos == 'pos':
                target_joints[5] += 0.01
            else:
                target_joints[5] = target_joints[5] - 0.01

        # self.rtde_c.speedJ(target_vel, self.move_acceleration, 0.001)
        self.rtde_c.moveJ(target_joints, self.move_velocity, self.move_acceleration, True)
        return
    
    def limitCheck(self):
        limit_list = []
        for i, j in enumerate(self.current_joint_values):
            if (j < (self.joint_upper_limits[5] - self.buffer_limit)) and (j > (self.joint_lower_limits[i] + self.buffer_limit)):
                limit_list.append(True)
            else:
                limit_list.append(False)
        
        if all(limit_list):
            return True
        else:
            print("Stopping before singularity")
            return False

    def vel_polar(self, coord, pos):
        
        target_vel = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        angular_velocity = self.move_velocity
        radius = self.current_polar[0]
        
        if coord == 'radius':
            if pos == 'pos':
                target_vel[0] = self.move_velocity* np.cos(self.current_polar[1])
                target_vel[1] = self.move_velocity* np.sin(self.current_polar[1])
            
            else:
                target_vel[0] = -self.move_velocity* np.cos(self.current_polar[1])
                target_vel[1] = -self.move_velocity* np.sin(self.current_polar[1])

        elif coord == 'theta':
            if pos == 'pos':
                target_vel[0] = -self.move_velocity * np.sin(self.current_polar[1])
                target_vel[1] = self.move_velocity * np.cos(self.current_polar[1])

            else:
                target_vel[0] = self.move_velocity * np.sin(self.current_polar[1])
                target_vel[1] = -self.move_velocity * np.cos(self.current_polar[1])
        
        elif coord == 'z':
            if pos == 'pos':
                target_vel[2] = self.move_velocity
            else:
                target_vel[2] = -self.move_velocity
       
        elif coord == 'a6':
            if pos == 'pos':
                target_vel[5] = self.move_velocity*5
            else:
                target_vel[5] = -self.move_velocity*5
        
        self.rtde_c.jogStart(speeds = target_vel)
        return

    def zero_velocity(self):
        self.rtde_c.jogStart(speeds = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        # self.rtde_c.speedJ(qd = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
        return

    def move_y(self, pos):
        target_pose = self.current_global_pose
        target_pose[0] += self.move_dist
        self.rtde_c.moveL(target_pose, self.move_velocity, self.move_acceleration, True)
        return

    def stop(self):
        self.rtde_c.stopL(self.move_acceleration)
        return
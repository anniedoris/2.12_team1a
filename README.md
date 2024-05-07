# 2.12_team1a - Repo for final project code!

Note that there are two folders: ```mobile_robot``` and ```ur5```. Please add code to the relevant folder.

## Mobile Robot

### List of Code
Below is a list of files and what they control for the mobile robot. Two files are required to run the controller, and four files are required to run the robot. For the Intel RealSense camera, terminal commands are sufficient to stream video to a PC. 

- Controller: ```controller_main.cpp``` and ```controller_wireless.cpp```
- Robot: ```robot_drive.cpp```, ```robot_main.cpp```, ```robot_motion_control.cpp```, and ```robot_wireless.cpp```
- SLAM

### How to Run the Code
To drive the mobile robot with the joystick: 
1. Find the mac address of the robot and controller by running ```get_mac.cpp``` on the controller and robot.
2. Enter the mac address in ```wireless.h```
	Set const uint8_t controllerAddr[] = controller mac address 
	Set const uint8_t robotAddr[] = robot mac address 
3. You need ```robot_pinout.h```, ```robot_motion_control.h```, ```robot_drive.h```, ```controller_pinout.h```, ```wireless.h``` and ```wireless.cpp``` as header and .cpp files.
4. Put ```robot_drive.cpp```, ```robot_main.cpp```, ```robot_motion_control.cpp``` and ```robot_wireless.cpp``` in the robot folder. Upload all these files to the mobile robot's ESP32. 
5. Put ```controller_main.cpp``` and ```controller_wireless.cpp``` in the controller folder. Upload both files to the controller.
6. Move the joystick and the robot will be moving. 

To stream video from the RealSense camera to a PC:
* Follow this tutorial: https://jetsonhacks.com/2019/12/22/install-realsense-camera-in-5-minutes-jetson-nano/
* Make sure the RealSense camera is connected to the Jetson Orin Nano with 
1. Install FFmpeg using Homebrew on the PC and the Jetson Orin Nano.
2. Enter this into the terminal on the Jetson Orin Nano: ```ffmpeg -f v4l2 -i /dev/video4 -c:v libx264 -preset ultrafast -crf 25  -b:v 6M -f rtp rtp://192.168.217.137:2000``` (Check network settings on the PC to get the PC's IP address. Replace the numbers after ```rtp://``` with your PC's IP address.)
3. Enter the terminal command ```ifconfig``` on the Jetson's terminal to confirm the Jetson Orin Nano IP address.
4. Replace the numbers after ```rtp://``` in the following text with the IP address of the PC: ```ffmpeg -f v4l2 -i /dev/video4 -c:v libx264 -preset ultrafast -crf 25  -b:v 6M -f rtp rtp://192.168.217.137:2000```. Run this command in the Jetson's terminal.
5. Step 4 generates values for a ```.sdp``` file. Copy the terms and save them as .sdp (in this case we saved them as ```real.sdp```. 
6. Run this command in the PC's terminal: ```ffplay -protocol_whitelist file,udp,rtp -i stream_ip.sdp```
7. Run this command in the Jetson's terminal (substitute the IP address with the PC's IP address): ```ffmpeg -f v4l2 -i /dev/video4 -c:v libx264 -preset ultrafast -crf 25  -b:v 6M -f rtp rtp://192.168.217.137:2000```
8. Video will stream from the camera to the PC screen. 

To run SLAM code:
1. Install the following: ```OpenCV```, ```Pangolin```, ```Eigen3```, ```DBoW2```, ```g2o```
2. Ensure the video stream is running from the Intel RealSense camera (see previous section). Turn each frame of the video into a ```.png``` file using the steps in the previous section (use ffmpeg). These images will be fed into the SLAM algorithm. 
3. Open terminal and navigate to the ```ORB_SLAM2-master``` directory.
3. Execute the following command in terminal: ```../Tunnel/Monocular/mono_tum Vocabulary/ORBvoc.txt ../Tunnel/Monocular/tunnel.yaml ../Tunnel/Monocular/```

* The ```Tunnel``` folder also includes images and configuration data from the mapping that was performed with the mobile robot. 

## UR5

### List of Code
Below is a list of files and what they control on the UR5.

**End effector control:**

- IR control: ```ur5/CPP/src/test_code/ir_threshold.cpp```
- Gripper control: ```ur5/CPP/src/test_code/gripper.cpp```

**Arm control:**

- Motion control: ```ur5/Python/main.py```

### How to Run the Code

**End effector control:**
You will need two computers. One will manage IR, the other will manage electromagnet/gripper.

For IR control:
1. Open VSCode in the CPP folder.
2. Move the ```ur5/CPP/src/test_code/ir_threshold.cpp``` into the ```robot``` folder and upload to microcontroller on the end effector. 
3. Reset microcontroller.
4. Open serial monitor on computer. You should see print outs of the IR readings.

For gripper control:
1. Open VSCode in the CPP folder.
2. Move the ```gripper.cpp``` into the ```robot``` folder and upload to microcontroller connected to the two power supplies, servos, and electromagnet.
3. Reset microcontroller. 
4. Open serial monitor on computer. 
5. Press the "i" key to move the gripper to its closed (inner) position. Press the "o" key to move the gripper to its open (outer) position. Press the "m" key to move the gripper to its middle (halfway open) position.
6. Press the "1" key to turn on the electromagnet. Press the "0" key to turn off the electromagnet. 

**Motion control:**

1. Ethernet connect your computer to the UR5.
2. ```cd``` into the ```ur5/Python/``` folder and run ```main.py```
3. The robot should move to an initial home position. You can then run any of the following commands:

- Theta cylindrical coordinates (relative to robot base): left/right arrow keys
- Radius cylindrical coordinates (in/out from robot base): up/down arrow keys
- Z cylindrical coordinates (height control): q/a keys
- Speed control: 1, 2, and 3 keys (increasing speed)
- Rotating end effector: 0/9 keys
- Pre-defined house positions: z (left house), x (middle house), c (right house) keys
- Pre-defined z heights: v (100 mm z height), f (650 mm height) keys

## Git best practices

Before you start doing any work, make sure that you ```git pull```.

To commit your changes and commit them often!!!

To do so, do the following:

```git status``` to see what changes you have relative to the remote. You should see some things show up as red. If they are red, they will not be pushed to the remote. To add the files you want to push to the remote, do:

```git add 'file_name```. If you run ```git status``` again you should see that the file has turned green! Do this for each file you want to add.

Next, run ```git commit -m "type a message describing what you are adding"```.

Finally, run ```git push``` to send your changes to main.
Mobile Robot Code Instructions

1. Find the mac address of the robot and controller by running get_mac.cpp on the controller and robot.
2. Enter the mac address in wireless.h
	Set const uint8_t controllerAddr[] = controller mac address 
	Set const uint8_t robotAddr[] = robot mac address 
3. You need robot_pinout.h, robot_motion_control.h, robot_drive.h, controller_pinout.h wireless.h and wireless.cpp as header and cpp files.
4. Put robot_drive.cpp, robot_main.cpp, robot_motion_control.cpp and robot_wireless.cpp in the robot folder. Upload all these files to the mobile robot. 
5. Put controller_main.cpp and controller_wireless.cpp in the controller folder. Upload both files to the controller.
6. Move the joystick and the robot will be moving. 

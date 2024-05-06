//Change made by Joo Won Lee to allow only 2 active motors
#ifndef ROBOT_DRIVE_H
#define ROBOT_DRIVE_H

#define NUM_MOTORS 2 //changed from 4 to 2

#define Kp 0.25
#define Ki 0.01
#define Kd 0
#define pidTau 0.1

#define MAX_FORWARD 10
#define MAX_TURN 4

void setupDrive();
void updateSetpoints(double left, double right);
void updatePIDs();

#endif // ROBOT_DRIVE_H
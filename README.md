# 2.12_team1a - Repo for final project code!

Note that there are two folders: ```mobile_robot``` and ```ur5```. Please add code to the relevant folder.

## Mobile Robot

### List of Code

### How to Run the Code

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
2. Move the ```ur5/CPP/src/test_code/ir_threshold.cpp``` into the ```robot``` folder and upload to microcontrolelr on the end effector. 
3. Reset microcontroller.
4. Open serial monitor on computer. You should see print outs of the IR readings.

For gripper control:
MICHAEL TODO

**Motion control:**

1. Ethernet connect your computer to the UR5.
2. ```cd``` into the ```ur5/Python/``` folder and run ```main.py```
3. The robot should move to an initial home position. You can then run any of the following commands:

- Theta cylindrical coordaintes (relative to robot base): left/right arrow keys
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
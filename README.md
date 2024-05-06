# 2.12_team1a - Repo for final project code!

Note that there are two folders: ```mobile_robot``` and ```ur5```. Please add code to the relevant folder.

## Mobile Robot

### List of Code

### How to Run the Code

## UR5

### List of Code
Below is a list of files and what they control on the UR5.

End effector control:

- IR control: ```ur5/CPP/src/test_code/ir_threshold.cpp```
- Gripper control: ```ur5/CPP/src/test_code/gripper.cpp```

Arm control:

- Motion control: ```ur5/Python/main.py```

### How to Run the Code

## Git best practices

Before you start doing any work, make sure that you ```git pull```.

To commit your changes and commit them often!!!

To do so, do the following:

```git status``` to see what changes you have relative to the remote. You should see some things show up as red. If they are red, they will not be pushed to the remote. To add the files you want to push to the remote, do:

```git add 'file_name```. If you run ```git status``` again you should see that the file has turned green! Do this for each file you want to add.

Next, run ```git commit -m "type a message describing what you are adding"```.

Finally, run ```git push``` to send your changes to main.
import rtde_control
rtde_c = rtde_control.RTDEControlInterface("169.254.157.0")
x = -0.143
y = -0.435
z = 0.2
rtde_c.moveL([x, y, z, -0.001, 3.12, 0.04], 0.5, 0.3)
while True:
    inp = input('move direction:')
    print(inp)
    if inp == 'q':
        x= x + 0.1
    if inp == 'a':
        x= x - 0.1
    if inp == 'w':
        y= y + 0.1
    if inp == 's':
        y= y - 0.1
    if inp == 'e':
        z= z + 0.1
    if inp == 'd':
        z= z - 0.1
    rtde_c.moveL([x, y, z, -0.001, 3.12, 0.04], 0.5, 0.3)

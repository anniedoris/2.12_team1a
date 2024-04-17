import rtde_control
import rtde_receive

rtde_c = rtde_control.RTDEControlInterface("169.254.157.0")
rtde_r = rtde_receive.RTDEReceiveInterface("169.254.157.0")

# Get current joint angles
init_q = rtde_r.getActualQ()

print(init_q)
print(type(init_q))

# # Get new q coordinates
new_q = init_q[:]
new_q[4] += 0.2

# rtde_c.moveJ()
# print(init_q)
rtde_c.moveJ(new_q)
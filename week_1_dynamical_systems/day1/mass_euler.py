import numpy as np
import matplotlib.pyplot as plt

m = 2
u = 4
del_t = 0.01
pk = 0
vk = 0
sim_time = 2
time = []
position = []
velocity = []

for i in np.arange(0,sim_time,del_t):
    a = u/m
    time.append(i)
    v_next = vk + a * (del_t)
    velocity.append(v_next)
    p_next = pk + vk * (del_t)
    position.append(p_next)
    pk = p_next
    vk = v_next
    print(f"Next timestep:", i, f"| Position:", p_next, f"| Velocity:", v_next)

print(f"Time: ", time)
print(f"velocity: ", velocity)
print(f"Position: ", position)

plt.title("Position vs Time")
plt.xlabel("Time")
plt.ylabel("Position")

plt.plot(time, position)

plt.grid()


plt.show()

plt.title("Velocity vs Time")
plt.xlabel("Time")
plt.ylabel("Velocity")

plt.plot(time, velocity)

plt.grid()


plt.show()
 
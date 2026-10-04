import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

m = 2

del_t = 0.1
pk = 0
vk = 0
sim_time = 30
# reference = 10 #For regulation
Kp = 0.5
time = []
position = []
velocity = []
reference2 = []
error2 = []

for i in np.arange(0,sim_time,del_t):
    reference = 10 * np.sin(i) #For Tracking
    time.append(i)
    reference2.append(reference)
    error = reference - pk
    error2.append(error)
    u= Kp *error
    a = u/m
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

plt.title("Error vs Time")
plt.xlabel("Error")
plt.ylabel("Time")
plt.plot(time, error2, label = "Error")
plt.show()

plt.title("Position vs Time")
plt.xlabel("Time")
plt.ylabel("Position")

plt.plot(time, position, label = "Position")
plt.plot(time,reference2, label = "Reference")
plt.legend()

plt.grid()
plt.show()

plt.title("Velocity vs Time")
plt.xlabel("Time")
plt.ylabel("Velocity")

plt.plot(time, velocity)
plt.legend()
plt.grid()


plt.show()


fig, ax = plt.subplots()

ax.set_xlim(0, sim_time)
ax.set_ylim(-100, 100)

ax.set_xlabel("Time (s)")
ax.set_ylabel("Position (m)")
ax.set_title(f"P Controller — Kp = {Kp}")

reference_line, = ax.plot([], [], label="Reference")
position_line, = ax.plot([], [], label="Position")

ax.legend()
ax.grid()

def update(frame):
    reference_line.set_data(time[:frame], reference2[:frame])
    position_line.set_data(time[:frame], position[:frame])
    return reference_line, position_line

animation = FuncAnimation(
    fig,
    update,
    frames=len(time),
    interval=50,
    blit=True
)

animation.save(
    f"p_controller_Kp_{Kp}.gif",
    writer=PillowWriter(fps=20)
)

plt.show()
 
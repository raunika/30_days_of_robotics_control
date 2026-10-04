import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


# System parameters
m = 2
b = 1.0


# Simulation parameters

del_t = 0.1
sim_time = 30
reference = 10


# PID gains

Kp = 0.5
Ki = 0.1
Kd = 2.0


# Initial conditions

pk = 0
vk = 0

integral = 0
previous_error = 0


# Data storage

time = []
position = []
velocity = []
reference_data = []
error_data = []
# Simulation

for i in np.arange(0, sim_time, del_t):

    # Reference
    reference_data.append(reference)
    time.append(i)

    # Error
    error = reference - pk
    error_data.append(error)

    # Integral
    integral += error * del_t

    # Derivative
    derivative = (error - previous_error) / del_t

    # PID controller
    u = (
        Kp * error
        + Ki * integral
        + Kd * derivative
    )

    # System dynamics
    a = (u - b * vk) / m

    # Update velocity
    v_next = vk + a * del_t

    # Update position
    p_next = (
        pk
        + vk * del_t
        + 0.5 * a * del_t**2
    )

    # Store
    velocity.append(v_next)
    position.append(p_next)

    # Update state
    pk = p_next
    vk = v_next

    # Update previous error
    previous_error = error


# Error plot

plt.figure()

plt.title("Error vs Time")
plt.xlabel("Time (s)")
plt.ylabel("Error (m)")

plt.plot(time, error_data)

plt.grid()
plt.show()


# Position plot

plt.figure()

plt.title("PID Position Control")
plt.xlabel("Time (s)")
plt.ylabel("Position (m)")

plt.plot(time, position, label="Position")
plt.plot(time, reference_data, label="Reference")

plt.legend()
plt.grid()
plt.show()


# Velocity plot

plt.figure()

plt.title("Velocity vs Time")
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")

plt.plot(time, velocity)

plt.grid()
plt.show()

#P vs PI vs PD vs PID

def simulate_controller(Kp, Ki, Kd):

    pk = 0
    vk = 0

    integral = 0
    previous_error = 0

    time = []
    position = []
    velocity = []
    error_data = []

    for i in np.arange(0, sim_time, del_t):

        error = reference - pk

        integral += error * del_t

        derivative = (error - previous_error) / del_t

        u = (
            Kp * error
            + Ki * integral
            + Kd * derivative
        )

        a = (u - b * vk) / m

        v_next = vk + a * del_t

        p_next = (
            pk
            + vk * del_t
            + 0.5 * a * del_t**2
        )

        time.append(i)
        position.append(p_next)
        velocity.append(v_next)
        error_data.append(error)

        pk = p_next
        vk = v_next
        previous_error = error

    return time, position, velocity, error_data

controllers = {
    "P": (0.5, 0, 0),
    "PI": (0.5, 0.1, 0),
    "PD": (0.5, 0, 2),
    "PID": (0.5, 0.1, 2)
}

results = {}

for name, gains in controllers.items():

    Kp, Ki, Kd = gains

    results[name] = simulate_controller(
        Kp, Ki, Kd
    )

plt.figure()

for name, data in results.items():

    time = data[0]
    position = data[1]

    plt.plot(
        time,
        position,
        label=name
    )

plt.axhline(
    reference,
    linestyle="--",
    label="Reference"
)

plt.xlabel("Time (s)")
plt.ylabel("Position (m)")
plt.title("P vs PI vs PD vs PID")

plt.legend()
plt.grid()
plt.show()

for name, data in results.items():

    time = data[0]
    error_data = data[3]

    plt.plot(
        time,
        error_data,
        label=name
    )


plt.xlabel("Time (s)")
plt.ylabel("Error (m)")
plt.title("P vs PI vs PD vs PID")

plt.legend()
plt.grid()
plt.show()

for name, data in results.items():

    time = data[0]
    velocity = data[2]

    plt.plot(
        time,
        velocity,
        label=name
    )


plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.title("P vs PI vs PD vs PID")

plt.legend()
plt.grid()
plt.show()

fig, ax = plt.subplots()

ax.set_xlim(0, sim_time)
ax.set_ylim(
    min(min(data[1]) for data in results.values()) - 1,
    max(max(data[1]) for data in results.values()) + 1
)

ax.set_xlabel("Time (s)")
ax.set_ylabel("Position (m)")
ax.set_title("P vs PI vs PD vs PID — Position")

ax.axhline(reference, linestyle="--", label="Reference")

lines = {}

for name in results:
    line, = ax.plot([], [], label=name)
    lines[name] = line

ax.legend()
ax.grid()


def update_position(frame):

    for name, data in results.items():

        time = data[0]
        position = data[1]

        lines[name].set_data(
            time[:frame],
            position[:frame]
        )

    return lines.values()


animation = FuncAnimation(
    fig,
    update_position,
    frames=len(time),
    interval=50,
    blit=True
)

animation.save(
    "pid_position_comparison.gif",
    writer=PillowWriter(fps=20)
)

plt.show()

fig, ax = plt.subplots()

ax.set_xlim(0, sim_time)
ax.set_ylim(
    min(min(data[3]) for data in results.values()) - 1,
    max(max(data[3]) for data in results.values()) + 1
)

ax.set_xlabel("Time (s)")
ax.set_ylabel("Error (m)")
ax.set_title("P vs PI vs PD vs PID — Error")

lines = {}

for name in results:
    line, = ax.plot([], [], label=name)
    lines[name] = line

ax.legend()
ax.grid()


def update_error(frame):

    for name, data in results.items():

        time = data[0]
        error = data[3]

        lines[name].set_data(
            time[:frame],
            error[:frame]
        )

    return lines.values()


animation = FuncAnimation(
    fig,
    update_error,
    frames=len(time),
    interval=50,
    blit=True
)

animation.save(
    "pid_error_comparison.gif",
    writer=PillowWriter(fps=20)
)

plt.show()

fig, ax = plt.subplots()

ax.set_xlim(0, sim_time)
ax.set_ylim(
    min(min(data[2]) for data in results.values()) - 1,
    max(max(data[2]) for data in results.values()) + 1
)

ax.set_xlabel("Time (s)")
ax.set_ylabel("Velocity (m/s)")
ax.set_title("P vs PI vs PD vs PID — Velocity")

lines = {}

for name in results:
    line, = ax.plot([], [], label=name)
    lines[name] = line

ax.legend()
ax.grid()


def update_velocity(frame):

    for name, data in results.items():

        time = data[0]
        velocity = data[2]

        lines[name].set_data(
            time[:frame],
            velocity[:frame]
        )

    return lines.values()


animation = FuncAnimation(
    fig,
    update_velocity,
    frames=len(time),
    interval=50,
    blit=True
)

animation.save(
    "pid_velocity_comparison.gif",
    writer=PillowWriter(fps=20)
)

plt.show()




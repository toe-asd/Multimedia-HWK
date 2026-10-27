import numpy as np
import matplotlib.pyplot as plt
from hwk1_1 import bezier_formula


# Three Bezier segments:
# one smooth join and one corner join


# Segment 1
p1_0 = np.array([50.0, 250.0])
p1_1 = np.array([100.0, 100.0])
p1_2 = np.array([180.0, 100.0])
p1_3 = np.array([230.0, 200.0])

# Segment 2 - smooth with segment 1
p2_0 = p1_3.copy()
p2_1 = np.array([280.0, 300.0])
p2_2 = np.array([350.0, 300.0])
p2_3 = np.array([400.0, 200.0])

# Segment 3 - corner with segment 2
p3_0 = p2_3.copy()
p3_1 = np.array([400.0, 100.0])
p3_2 = np.array([500.0, 100.0])
p3_3 = np.array([550.0, 250.0])


# Calculate curves
curve1 = bezier_formula(
    p1_0, p1_1, p1_2, p1_3, 1000
)

curve2 = bezier_formula(
    p2_0, p2_1, p2_2, p2_3, 1000
)

curve3 = bezier_formula(
    p3_0, p3_1, p3_2, p3_3, 1000
)


# Direction vectors

join1_in = p1_3 - p1_2
join1_out = p2_1 - p2_0

join2_in = p2_3 - p2_2
join2_out = p3_1 - p3_0


print("===== Join 1 =====")
print("incoming direction =", join1_in)
print("outgoing direction =", join1_out)

print()

print("===== Join 2 =====")
print("incoming direction =", join2_in)
print("outgoing direction =", join2_out)


# Plot three segments

plt.figure(figsize=(10, 6))

plt.plot(
    curve1[:, 0],
    curve1[:, 1],
    linewidth=3,
    label="Bezier Segment 1"
)

plt.plot(
    curve2[:, 0],
    curve2[:, 1],
    linewidth=3,
    label="Bezier Segment 2"
)

plt.plot(
    curve3[:, 0],
    curve3[:, 1],
    linewidth=3,
    label="Bezier Segment 3"
)


# Smooth join direction lines
plt.plot(
    [p1_2[0], p1_3[0], p2_1[0]],
    [p1_2[1], p1_3[1], p2_1[1]],
    "o--",
    color="black",
    label="Direction Lines"
)


# Corner join direction lines
plt.plot(
    [p2_2[0], p2_3[0]],
    [p2_2[1], p2_3[1]],
    "o--",
    color="black"
)

plt.plot(
    [p3_0[0], p3_1[0]],
    [p3_0[1], p3_1[1]],
    "o--",
    color="black"
)


# Mark joins
plt.scatter(
    [p1_3[0]],
    [p1_3[1]],
    s=100,
    color="red",
    label="Smooth Join"
)

plt.scatter(
    [p2_3[0]],
    [p2_3[1]],
    s=100,
    color="purple",
    label="Corner Join"
)


plt.title(
    "Three Bezier Segments: Smooth Join and Corner Join"
)

plt.xlabel("X")
plt.ylabel("Y")

plt.axis("equal")
plt.grid()
plt.legend()

plt.show()


# Part 1.3 (2)
# Equal-length vs Unequal-length direction lines

# Common join point
J = np.array([300.0, 200.0])

# Left Bezier segment

q1_0 = np.array([100.0, 250.0])
q1_1 = np.array([150.0, 100.0])
q1_2 = np.array([250.0, 150.0])
q1_3 = J.copy()


# Incoming direction
# J - q1_2 = (50, 50)


# Equal-length version


q2_0 = J.copy()

# Same direction and same length
q2_1 = np.array([350.0, 250.0])

q2_2 = np.array([450.0, 300.0])
q2_3 = np.array([500.0, 200.0])


# Unequal-length version

q3_0 = J.copy()

# Same direction, but twice the length
q3_1 = np.array([400.0, 300.0])

q3_2 = np.array([450.0, 300.0])
q3_3 = np.array([500.0, 200.0])


# Calculate curves
left_curve = bezier_formula(
    q1_0, q1_1, q1_2, q1_3, 1000
)

equal_curve = bezier_formula(
    q2_0, q2_1, q2_2, q2_3, 1000
)

unequal_curve = bezier_formula(
    q3_0, q3_1, q3_2, q3_3, 1000
)


# Direction vectors


incoming = q1_3 - q1_2
equal_out = q2_1 - q2_0
unequal_out = q3_1 - q3_0


print()
print("===== Equal vs Unequal =====")

print("Incoming direction =", incoming)
print("Equal outgoing direction =", equal_out)
print("Unequal outgoing direction =", unequal_out)


# Calculate lengths

incoming_length = (
    incoming[0] ** 2 +
    incoming[1] ** 2
) ** 0.5

equal_length = (
    equal_out[0] ** 2 +
    equal_out[1] ** 2
) ** 0.5

unequal_length = (
    unequal_out[0] ** 2 +
    unequal_out[1] ** 2
) ** 0.5


print()

print("Incoming length =", incoming_length)
print("Equal outgoing length =", equal_length)
print("Unequal outgoing length =", unequal_length)


# Plot equal and unequal versions side by side

fig, axes = plt.subplots(
    1,
    2,
    figsize=(12, 5)
)


# Left figure: Equal length

axes[0].plot(
    left_curve[:, 0],
    left_curve[:, 1],
    linewidth=3,
    label="Left Segment"
)

axes[0].plot(
    equal_curve[:, 0],
    equal_curve[:, 1],
    linewidth=3,
    label="Right Segment"
)


# Direction lines
axes[0].plot(
    [
        q1_2[0],
        q1_3[0],
        q2_1[0]
    ],
    [
        q1_2[1],
        q1_3[1],
        q2_1[1]
    ],
    "o--",
    color="black",
    label="Direction Lines"
)


axes[0].scatter(
    J[0],
    J[1],
    s=100,
    color="red",
    label="Join"
)


axes[0].set_title(
    "Equal-Length Direction Lines"
)

axes[0].set_xlabel("X")
axes[0].set_ylabel("Y")

axes[0].axis("equal")
axes[0].grid()
axes[0].legend()

# Right figure: Unequal length
axes[1].plot(
    left_curve[:, 0],
    left_curve[:, 1],
    linewidth=3,
    label="Left Segment"
)

axes[1].plot(
    unequal_curve[:, 0],
    unequal_curve[:, 1],
    linewidth=3,
    label="Right Segment"
)


# Direction lines
axes[1].plot(
    [
        q1_2[0],
        q1_3[0],
        q3_1[0]
    ],
    [
        q1_2[1],
        q1_3[1],
        q3_1[1]
    ],
    "o--",
    color="black",
    label="Direction Lines"
)


axes[1].scatter(
    J[0],
    J[1],
    s=100,
    color="red",
    label="Join"
)


axes[1].set_title(
    "Unequal-Length Direction Lines"
)

axes[1].set_xlabel("X")
axes[1].set_ylabel("Y")

axes[1].axis("equal")
axes[1].grid()
axes[1].legend()


plt.tight_layout()
plt.show()
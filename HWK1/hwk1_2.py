import numpy as np
import matplotlib.pyplot as plt
from hwk1_1 import bezier_formula, split_bezier, midpoint_curve
p0 = np.array([50.0,300.0])
p1 = np.array([150.0,50.0]) 
p2 = np.array([350.0,50.0])
p3 = np.array([450.0,300.0])

def max_sample_gap(curve):
    max_gap = 0
    for i  in range(len(curve)-1):
        dx = curve[i+1][0]-curve[i][0]
        dy = curve[i+1][1]-curve[i][1]
        distance =(dx**2 + dy**2)**0.5
        if distance> max_gap:
            max_gap = distance
    return max_gap

def find_N(p0,p1,p2,p3,start=1000,step=100):
    
    num_points = start
    num_list = []
    gap_list = []

    while True:
        curve = bezier_formula(p0,p1,p2,p3,num_points)
        max_gap = max_sample_gap(curve)
        num_list.append(num_points)
        gap_list.append(max_gap)
        print(
            "num_points =",
             num_points,
            "max gap =",
            max_gap
        )
        if max_gap<0.1:
            return num_points, max_gap, num_list, gap_list
        num_points+=step
  
n, gap, num_list, gap_list = find_N(
    p0, p1, p2, p3,
    start=1000,
    step=100
)
plt.plot(
    num_list,
    gap_list,
    "o-",
    markersize=3
)

plt.axhline(
    y=0.1,
    color="red",
    linestyle="--",
    label="0.1 px threshold"
)

plt.xlabel("Number of Formula Samples")
plt.ylabel("Maximum Consecutive-Point Gap (px)")
plt.title("Formula Sampling Density")

plt.grid()
plt.legend()
plt.show()

def point_to_segment_distance(p, a, b):

    ab_x = b[0] - a[0]
    ab_y = b[1] - a[1]

    ap_x = p[0] - a[0]
    ap_y = p[1] - a[1]

    ab_length_square = ab_x**2 + ab_y**2

    t = (ap_x * ab_x + ap_y * ab_y) / ab_length_square

    if t < 0:
        closest_x = a[0]
        closest_y = a[1]

    elif t > 1:
        closest_x = b[0]
        closest_y = b[1]

    else:
        closest_x = a[0] + t * ab_x
        closest_y = a[1] + t * ab_y

    dx = p[0] - closest_x
    dy = p[1] - closest_y

    distance = (dx**2 + dy**2) ** 0.5

    return distance

def distance_to_polyline(p,polyline):
    min_distance = float("inf")
    for i in range (len(polyline) - 1):
        a = polyline[i]
        b = polyline[i+1]
        distance = point_to_segment_distance(
            p,a,b
        )
        if distance < min_distance:
            min_distance = distance
    return min_distance

def max_error(formula_curve, polyline):

    max_distance = 0

    for p in formula_curve:

        distance = distance_to_polyline(
            p, polyline
        )

        if distance > max_distance:
            max_distance = distance

    return max_distance

depth_list = []
error_list = []
for depth in range(0, 10):

    mid_points = midpoint_curve(
        p0, p1, p2, p3,
        depth
    )

    mid_points = np.array(mid_points)

    answer = bezier_formula(
    p0, p1, p2, p3,
    n
    )

    error = max_error(
        answer,
        mid_points
    )
    depth_list.append(depth)
    error_list.append(error)


    print(
        "depth =",
        depth,
        "max error =",
        error
    )


plt.plot(
    depth_list,
    error_list,
    "o-"
)

plt.xlabel("Subdivision Depth")
plt.ylabel("Maximum Error (px)")
plt.title("Convergence of Midpoint Subdivision")

plt.grid()
plt.show()
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
" The cubic formula (Figure 1, left): C(t) = (1−t)³b₀ + 3t(1−t)²b₁ + 3t²(1−t)b₂ + t³b₃ "
def bezier_formula(p0,p1,p2,p3,num_points):
    curve=[]
    for i in range(num_points):
        t = i / (num_points - 1)#要分幾部分
        point = ((1-t)**3 *p0 + 3*t*(1-t)**2*p1 + 3*t**2*(1-t)*p2 + t**3*p3)

        curve.append(point)

    return np.array(curve)

def split_bezier(p0,p1,p2,p3):
    a = (p0+p1)/2
    b = (p1+p2)/2
    c = (p2+p3)/2

    d = (a+b)/2
    e = (b+c)/2

    f = (d+e)/2

    left = (p0,a,d,f)
    right = (f,e,c,p3)
    return left,right

def midpoint_curve(p0,p1,p2,p3,depth):
    if depth ==0:
        return [p0,p3]
    left, right = split_bezier(p0,p1,p2,p3)

    left_points= midpoint_curve(*left,depth-1)
    right_points= midpoint_curve(*right,depth-1)
    return left_points[:-1]+ right_points

    
if __name__ == "__main__":

 p0 = np.array([50.0,300.0])       
 p1 = np.array([150.0, 50.0])
 p2 = np.array([350.0, 50.0])
 p3 = np.array([450.0, 300.0])
#A圖
 answer = bezier_formula(p0,p1,p2,p3,1000)
 plt.plot(
    answer[:, 0],
      answer[:, 1],
      color="red",
      label = "Bezier Curve")
 control_points = np.array([p0,p1,p2,p3])
 plt.plot(
    control_points[:, 0],
    control_points[:, 1],
    label="Control Points"
 )

 plt.title("Bezier Curve")
 plt.axis("equal")
 plt.legend()
 plt.show()
# B圖
 mid_points = midpoint_curve(p0,p1,p2,p3,10)
 mid_points = np.array(mid_points)
 plt.plot(
    mid_points[:, 0],
    mid_points[:, 1],
    "o--",
    color="blue",
    label="Midpoint subdivision"
 )

 plt.axis("equal")
 plt.legend()
 plt.show()

# A and B  different
 answer = bezier_formula(p0,p1,p2,p3,1000)
 plt.plot(
    answer[:, 0],
      answer[:, 1],
      color="red",
      label = "Bezier Curve")
 control_points = np.array([p0,p1,p2,p3])
 plt.plot(
    control_points[:, 0],
    control_points[:, 1],
    label="Control Points"
 )
 mid_points = midpoint_curve(p0,p1,p2,p3,3)
 mid_points = np.array(mid_points)
 plt.plot(
    mid_points[:, 0],
    mid_points[:, 1],
    "o--",
    color="blue",
    label="Midpoint subdivision"
 )
 plt.title("Bezier Formula vs Midpoint Subdivision")
 plt.axis("equal")
 plt.legend()
 plt.show()
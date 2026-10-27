import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from hwk2_1 import scanline_fill,draw_path_arrows
# hwk2_3.py 所在位置：HWK/HWK2
current_dir = os.path.dirname(os.path.abspath(__file__))

# 往上一層到 HWK
hwk_dir = os.path.abspath(
    os.path.join(current_dir, "..")
)

# 告訴 Python 可以到 HWK 裡面找 module
sys.path.append(hwk_dir)
from HWK1.hwk1_1 import midpoint_curve

# 1. 畫出兩個CIRCLE 用midpoint curve and split 
def create_circle(x,y,r,depth):
    k = 0.5523*r
    top  = np.array([x,y-r],
            dtype="float"
        )
    right =  np.array([x+r,y],
            dtype="float"
        )
    bottom = np.array([x,y+r],
            dtype="float"
        )
    left =  np.array([x-r,y],
            dtype="float"
        )
    #找到4個點 有4段 curve
    segments = [
       #top-> right
       (top,
         np.array([x+k,y-r], dtype="float" ),
         np.array([x+r,y-k], dtype="float"),
        right    
        ),
        # right->bottom
        (right,
        np.array([x+r,y+k], dtype="float" ),
        np.array([x+k,y+r], dtype="float"),
        bottom    
        ),
        # bottom->left
        (bottom,
         np.array([x-k,y+r], dtype="float" ),
        np.array([x-r,y+k], dtype="float"),
         left
        ),
        # left-> top
        (left,
        np.array([x-r,y-k], dtype="float" ),
        np.array([x-k,y-r], dtype="float"),
        top   
        )  
    ]
    path = []
    for segment in segments:
        points = midpoint_curve(*segment,depth)
        if len(path) > 0:
         points = points[1:]
        path.extend(points)


    path = [(float(p[0]),float(p[1])) for p in path]

    return path
#計算某個點的winding number
def winding_target_point(subpaths,x,y):
   crossings = []
   for path in subpaths:
      for i in range(len(path)):
         x1,y1 = path[i]
         x2,y2 = path[(i+1)%len(path)]
         if y1 == y2 :
            continue
         if (y1<=y<y2) or (y2<=y<y1):
            x_cross= (x1+ (y - y1)* (x2 - x1)/ (y2 - y1))
            if y2>y1:
              change =+ 1
            else:
              change=-1
            crossings.append((x_cross,change))
   crossings.sort(key=lambda item:item[0])
   winding = 0
   for x_cross,change in crossings:
         if x_cross>x:
            break
         winding+=change
   return winding

if __name__=="__main__":
   width  = 500
   height = 500
   x =250
   y =250

   outer_r = 180
   inner_r = 90

   depth = 6
#建 outer and inner
   outer_circle = create_circle(
      x,y,outer_r,depth  
    )
   inner_circle = create_circle(
         x,y,inner_r,depth  
       )

   #if 同方向
   subpaths_same = [
      outer_circle,
      inner_circle
   ]
   canvas_same = scanline_fill(
      subpaths_same,
      width,
      height   
   )
   winding_same = winding_target_point(
      subpaths_same,x,y
   )
   print(
        "Same direction center winding =",
        winding_same
    )
   # 反方向
   inner_circle_reverse = list(reversed(inner_circle))

   subpaths_reverse = [
         outer_circle,
         inner_circle_reverse
      ]
   canvas_reverse = scanline_fill(
         subpaths_reverse,
         width,
         height   
      )
   winding_reverse = winding_target_point(
         subpaths_reverse,x,y
      )
   print(
           "reverse direction center winding =",
           winding_reverse
       )

#setting

   cmap = ListedColormap([
   "white",'blue'
    ])
#畫出same
  # =========================
# Figure 1：same direction
# =========================

   plt.figure(figsize=(7, 7))

   plt.imshow(
    canvas_same,
    cmap=cmap,
    origin="upper",
    vmin=0,
    vmax=255
)

   draw_path_arrows(
    outer_circle,
    step=16,
    color="red"
)

   draw_path_arrows(
    inner_circle,
    step=16,
    color="orange"
)

   plt.scatter(
    x,
    y,
    color="yellow",
    s=80,
    label=f"Center Winding = {winding_same}"
)

   plt.title(
    f"Same Direction, Center Winding = {winding_same}"
)

   plt.legend()
   plt.xlim(0, width)
   plt.ylim(height, 0)
   plt.axis("equal")


# =========================
# Figure 2：reverse direction
# =========================

   plt.figure(figsize=(7, 7))

   plt.imshow(
    canvas_reverse,
    cmap=cmap,
    origin="upper",
    vmin=0,
    vmax=255
)

   draw_path_arrows(
    outer_circle,
    step=16,
    color="red"
)

   draw_path_arrows(
    inner_circle_reverse,
    step=16,
    color="orange"
)

   plt.scatter(
    x,
    y,
    color="yellow",
    s=80,
    label=f"Center Winding = {winding_reverse}"
)

   plt.title(
    f"Reverse Inner Direction, Center Winding = {winding_reverse}"
)

   plt.legend()
   plt.xlim(0, width)
   plt.ylim(height, 0)
   plt.axis("equal")


   plt.show()



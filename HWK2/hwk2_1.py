import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
# 判斷圖片 Inside or Outside
def scanline_fill(subpaths,width,height):
    canvas = np.zeros((height,width),dtype=np.uint8)

    for y in range(height):
        crossing = []

        for path in subpaths:
            for i in range(len(path)):
                p1 = path[i]
                p2 = path[(i+1)%len(path)]
                x1,y1 = p1
                x2,y2 = p2

                if y1==y2:#水平
                    continue
                if (y1<=y<y2) or (y2<=y<y1): # 如果經過的是path左到右 or 右到左

                    x_cross = x1+(y-y1)*(x2-x1)/(y2-y1)#求 scanline 和 path的焦點
                
                    if(y2>y1):
                        change = +1
                    else:
                        change = -1
                    crossing.append((x_cross,change))
        crossing.sort(key=lambda item:item[0])#根據 x 排序
        winding = 0
        previous_x = 0

        for x_cross , change in crossing:
            current_x  =  int(np.ceil(x_cross))

            #判斷 winding 是否為0 判斷 inside outside
            if winding!=0: #inside
                start  = max(previous_x,0)
                end =  min (current_x,width)
                if start < end:
                    canvas[y,start:end] =255
            winding+=change
            previous_x = current_x
    return canvas

        
def get_scanline_info(path, y):
    crossings = []

    for i in range(len(path)):
        p1 = path[i]
        p2 = path[(i + 1) % len(path)]

        x1, y1 = p1
        x2, y2 = p2
         #下面依樣是判斷
        if y1 == y2:
            continue

        if (y1 <= y < y2) or (y2 <= y < y1):
            x_cross = x1 + (y - y1) * (x2 - x1) / (y2 - y1)

            if y2 > y1:
                change = +1
            else:
                change = -1

            crossings.append((x_cross, change))

    crossings.sort(key=lambda item: item[0])

    winding_steps = []
    winding = 0

    for x_cross, change in crossings:
        winding += change
        winding_steps.append((x_cross, change, winding))

    return crossings, winding_steps


if __name__ == "__main__":

 # test
 width = 500
 height = 500
 
 polygon = [
    (250, 50),
    (367, 410),
    (60, 188),
    (440, 188),
    (133, 410)
  ]

 subpaths = [polygon]

 canvas = scanline_fill(subpaths, width, height)

# 指定要觀察的 scanline
 test_y = 250
 crossings, winding_steps = get_scanline_info(polygon, test_y)

 print("Scanline y =", test_y)
 print("Crossings:")
 for x_cross, change in crossings:
    print("x =", x_cross, "change =", change)

 print("\nWinding steps:")
 for x_cross, change, winding in winding_steps:
    print("x =", x_cross, "change =", change, "winding =", winding)

 cmap = ListedColormap(["white", "blue"])

 plt.imshow(
    canvas,
    cmap=cmap,
    origin="upper",
    vmin=0,
    vmax=255
  )

# 顯示原始 path
 path_x = [p[0] for p in polygon] + [polygon[0][0]]
 path_y = [p[1] for p in polygon] + [polygon[0][1]]

 
# 顯示 scanline
 plt.axhline(
    y=test_y,
    color="green",
    linestyle="--",
    linewidth=2,
    label="Test Scanline"
 )
 
# 顯示 crossings 和 winding
 for x_cross, change, winding in winding_steps:
    plt.scatter(
        x_cross,
        test_y,
        color="orange",
        s=60
    )

    plt.text(
        x_cross + 5,
        test_y - 8,
        f"{change:+d}, w={winding}",
        color="black",
        fontsize=9
    )

 plt.title("Self-Intersecting Star Test")
 plt.axis("equal")
 plt.legend()
 plt.show()
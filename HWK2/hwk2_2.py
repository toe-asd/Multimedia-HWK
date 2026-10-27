from hwk2_1 import scanline_fill ,get_scanline_info
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

width = 500
height = 500
star=[
   (250, 50),
    (367, 410),
    (60, 188),
    (440, 188),
    (133, 410) 
]
subpaths = [star]

canvas = scanline_fill(
    subpaths,
    width,
    height
)
# star center 
center_x = 250
center_y = 250

crossings,winding_steps = get_scanline_info(
    star,
    center_y
)

center_winding = 0

for x_cross , change in crossings:
    if x_cross>center_x:
        break
    center_winding+=change

print(
    "Center winding number =",
    center_winding
)

#開畫
cmap = ListedColormap([
    "white",
    "blue"
])
plt.imshow(
    canvas,
    cmap=cmap,
    origin="upper",
    vmin = 0,
    vmax = 255
)
# Star path
path_x = [p[0] for p in star] + [star[0][0]]
path_y = [p[1] for p in star] + [star[0][1]]

plt.plot(
    path_x,
    path_y,
    color="red",
    linewidth=2,
    label="Star Path"
)


# Center point
plt.scatter(
    center_x,
    center_y,
    color="yellow",
    s=100,
    label=f"Center winding = {center_winding}"
)


plt.title("Part 2.2 - Self-Intersecting Star")
plt.axis("equal")
plt.legend()
plt.show()
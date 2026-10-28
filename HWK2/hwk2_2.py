from hwk2_1 import scanline_fill ,get_scanline_info
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

# 設定輸出像素陣列的寬度與高度
width = 500
height = 500
# 依序列出自交星形的頂點，交由掃描線函式閉合路徑
star=[
   (250, 50),
    (367, 410),
    (60, 188),
    (440, 188),
    (133, 410) 
]
subpaths = [star]

# 使用自行實作的非零 winding 掃描線填色，產生像素陣列
canvas = scanline_fill(
    subpaths,
    width,
    height
)
# star center 
center_x = 250
center_y = 250

# 取得通過星形中心的掃描線交點與 winding 變化
crossings,winding_steps = get_scanline_info(
    star,
    center_y
)

center_winding = 0

# 由左往右累計中心位置以前的交點，求得中心 winding number
for x_cross , change in crossings:
    if x_cross>center_x:
        break
    center_winding+=change

print(
    "Center winding number =",
    center_winding
)

#開畫
# 將背景與填色像素分別對應為白色與藍色
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
# 重複第一個頂點以閉合顯示用輪廓，這些座標不參與填色計算
path_x = [p[0] for p in star] + [star[0][0]]
path_y = [p[1] for p in star] + [star[0][1]]


# Center point
# 標記中心位置，並在圖例中顯示程式計算的 winding number
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
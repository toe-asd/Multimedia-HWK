import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

# 取得目前檔案位置，設定匯入共用填色模組的搜尋路徑
current_dir = os.path.dirname(
    os.path.abspath(__file__)
)

hwk_dir = os.path.abspath(
    os.path.join(current_dir, "..")
)

sys.path.append(hwk_dir)


from HWK2.hwk2_1 import scanline_fill


# 將每個頂點繞指定中心旋轉 degree 度，回傳旋轉後的路徑
def rotate_path(path, cx, cy, degree):

    # 將角度轉為弧度，供三角函式計算旋轉矩陣
    angle = math.radians(degree)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    new_path = []

    for x, y in path:

        # 將旋轉中心移到原點
        dx = x - cx
        dy = y - cy

        # rotation matrix
        new_x = (cx+ dx * cos_a- dy * sin_a)
        new_y = (cy+ dx * sin_a+ dy * cos_a)

        new_path.append( (new_x, new_y))

    return new_path


# 先以 k 倍解析度自行填色，再平均每個像素的 k × k 個子像素
def supersample_render(subpaths, width,height, k):
    scaled_subpaths = []

    # 將所有路徑座標放大 k 倍，對應高解析度像素網格
    for path in subpaths:

        scaled_path = []

        for x, y in path:

            scaled_path.append((x * k,y * k ))
        scaled_subpaths.append(scaled_path)

    high_width = width * k
    high_height = height * k

    # 呼叫共用掃描線實作，決定高解析度網格中哪些像素被覆蓋
    high_canvas = scanline_fill(
        scaled_subpaths,
        high_width,
        high_height
    )



    # 將陣列整理為原始列、子像素列、原始欄、子像素欄，平均子像素兩軸
    canvas = high_canvas.reshape(height,k,width,k).mean(axis=(1, 3))

    return canvas



if __name__ == "__main__":

    width = 500
    height = 500

    x = 250
    y = 250

    star = [
        (250, 50),
        (367, 410),
        (60, 188),
        (440, 188),
        (133, 410)
    ]

    # 將星形繞中心旋轉 5 度，觀察斜邊的鋸齒現象
    rotated_star = rotate_path(star, x,y,5)
    subpaths = [rotated_star]
    ks = [ 1,2,4,8]
    results = {}
    # 分別產生 k = 1、2、4、8 的像素結果
    for k in ks:
        canvas = supersample_render( subpaths,width, height,k )
        results[k] = canvas

    # 建立四個子圖，方便比較不同取樣倍率的結果
    fig, axes = plt.subplots(
        2,
        2,
        figsize=(10, 10)
    )


    # 顯示已自行計算的像素陣列，並標示對應倍率
    for ax, k in zip(axes.flat,ks):

        ax.imshow(
            results[k],
            cmap="gray",
            origin="upper",
            vmin=0,
            vmax=255
        )

        ax.set_title(
            f"k = {k}"
        )

        ax.axis("off")


    plt.suptitle(
        "Part 3.1 - Rotated Star Supersampling"
    )

    plt.tight_layout()

    plt.show()
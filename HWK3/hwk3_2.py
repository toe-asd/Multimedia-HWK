import os
import sys
import math
import time
import numpy as np
import matplotlib.pyplot as plt
from hwk3_1 import rotate_path,supersample_render


current_dir = os.path.dirname(
    os.path.abspath(__file__)
)

hwk_dir = os.path.abspath(
    os.path.join(current_dir, "..")
)

sys.path.append(hwk_dir)


from HWK2.hwk2_1 import scanline_fill


def find_shallowest_edge(path):

    min_slope = float("inf")

    best_p1 = None
    best_p2 = None


    for i in range(len(path)):

        p1 = path[i]

        p2 = path[ (i + 1) % len(path)]

        x1, y1 = p1
        x2, y2 = p2

        dx = x2 - x1
        dy = y2 - y1

        # vertical edge
        if abs(dx) ==0:
            continue

        slope = abs( dy / dx)
        if slope < min_slope:

            min_slope = slope

            best_p1 = p1
            best_p2 = p2


    return (best_p1,best_p2,min_slope)


def choose_test_position(p1,p2):

    x1, y1 = p1
    x2, y2 = p2


    # 靠近第一個 endpoint
    # 不要選 edge 中央
    t = 0.20


    test_x = (x1 + t * (x2 - x1))

    test_y = (y1+ t * (y2 - y1))


    row = int( round(test_y))

    return ( row,test_x)



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


    rotated_star = rotate_path(star,x,y,5)


    subpaths = [rotated_star]


    ks = [ 1,2,4,8 ]


    results = {}

    render_times = {}


    for k in ks:

        start = time.perf_counter()


        canvas = supersample_render(
            subpaths,
            width,
            height,
            k
        )


        end = time.perf_counter()


        results[k] = canvas

        render_times[k] = (
            end - start
        )


        print(
            f"k = {k}, "
            f"time = "
            f"{render_times[k]:.6f} sec"
        )


    # ========================================================
    # 3.2(a)
    # 找 shallowest edge
    # ========================================================

    p1, p2, slope = (find_shallowest_edge( rotated_star))

    print()
    print(
        "Shallowest edge"
    )

    print(
        "P1 =",
        p1
    )

    print(
        "P2 =",
        p2
    )

    print(
        "Slope =",
        slope
    )

    row, test_x = (choose_test_position(p1,p2))

    print(
        "Selected row =",
        row
    )


    # ========================================================
    # 只看 edge 附近
    # 避免其他 star edges 干擾
    # ========================================================

    x_min = max(
        0,
        int(test_x - 70)
    )

    x_max = min(
        width,
        int(test_x + 70)
    )


    x_values = np.arange(
        x_min,
        x_max
    )


    values_k1 = results[1][
        row,
        x_min:x_max
    ]


    values_k8 = results[8][
        row,
        x_min:x_max
    ]


    # ========================================================
    # 畫 row profile
    # ========================================================

    plt.figure(
        figsize=(10, 5)
    )


    plt.plot(
        x_values,
        values_k1,
        label="k = 1"
    )


    plt.plot(
        x_values,
        values_k8,
        label="k = 8"
    )


    plt.xlabel(
        "Pixel x"
    )

    plt.ylabel(
        "Pixel value"
    )

    plt.title(
        f"Part 3.2(a) - Row y = {row}"
    )

    plt.ylim(
        -10,
        265
    )

    plt.legend()

    plt.grid()


    # ========================================================
    # 3.2(b)
    # Render Time
    # ========================================================

    print()
    print(
        "Render time:"
    )


    for k in ks:

        print(
            f"k = {k}: "
            f"{render_times[k]:.6f} sec"
        )


    # ========================================================
    # 顯示 render time
    # ========================================================

    plt.figure(
        figsize=(7, 5)
    )


    plt.plot(
        ks,
        [
            render_times[k]
            for k in ks
        ],
        marker="o"
    )


    plt.xlabel(
        "k"
    )

    plt.ylabel(
        "Render Time (seconds)"
    )

    plt.title(
        "Part 3.2(b) - Render Time"
    )

    plt.grid()


    plt.show()
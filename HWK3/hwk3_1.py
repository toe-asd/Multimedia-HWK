import os
import sys
import math
import numpy as np
import matplotlib.pyplot as plt

current_dir = os.path.dirname(
    os.path.abspath(__file__)
)

hwk_dir = os.path.abspath(
    os.path.join(current_dir, "..")
)

sys.path.append(hwk_dir)


from HWK2.hwk2_1 import scanline_fill


def rotate_path(path, cx, cy, degree):

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


def supersample_render(subpaths, width,height, k):
    scaled_subpaths = []

    for path in subpaths:

        scaled_path = []

        for x, y in path:

            scaled_path.append((x * k,y * k ))
        scaled_subpaths.append(scaled_path)

    high_width = width * k
    high_height = height * k

    high_canvas = scanline_fill(
        scaled_subpaths,
        high_width,
        high_height
    )



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

    rotated_star = rotate_path(star, x,y,5)
    subpaths = [rotated_star]
    ks = [ 1,2,4,8]
    results = {}
    for k in ks:
        canvas = supersample_render( subpaths,width, height,k )
        results[k] = canvas

    fig, axes = plt.subplots(
        2,
        2,
        figsize=(10, 10)
    )


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
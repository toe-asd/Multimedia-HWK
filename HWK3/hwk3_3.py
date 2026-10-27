import os
import sys
import math
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



def create_wheel(cx, cy,radius,wedge_count):

    subpaths = []


    sector_angle = (
        2 * math.pi
        / wedge_count
    )

    # 因為 wedge 和 gap 一樣寬
    # 所以 wedge 佔一半
    wedge_angle = (sector_angle / 2)

    for i in range(wedge_count):

        # 每個 wedge 的中心角度
        center_angle = (
            i * sector_angle
        )


        angle1 = (
            center_angle
            - wedge_angle / 2
        )


        angle2 = (
            center_angle
            + wedge_angle / 2
        )


        p0 = (cx,cy)


        # circle point 1
        p1 = (
            cx
            + radius
            * math.cos(angle1),

            cy
            + radius
            * math.sin(angle1)
        )


        # circle point 2
        p2 = (
            cx
            + radius
            * math.cos(angle2),

            cy
            + radius
            * math.sin(angle2)
        )


        # 一個 wedge = triangle
        triangle = [
            p0,
            p1,
            p2
        ]


        subpaths.append(
            triangle
        )


    return subpaths



if __name__ == "__main__":

    width = 500
    height = 500


    cx = 250
    cy = 250


    radius = 210

    wedge_count = 48



    wheel = create_wheel(
        cx,
        cy,
        radius,
        wedge_count
    )


    print(
        "Number of wedges =",
        len(wheel)
    )



    wheel_k1 = supersample_render(
        wheel,
        width,
        height,
        1
    )


   

    wheel_k8 = supersample_render(
        wheel,
        width,
        height,
        8
    )


    fig, axes = plt.subplots(
        1,
        2,
        figsize=(12, 6)
    )


    # k = 1
    axes[0].imshow(
        wheel_k1,
        cmap="gray",
        origin="upper",
        vmin=0,
        vmax=255
    )

    axes[0].set_title(
        "Wheel - k = 1"
    )

    axes[0].axis("off")


    # k = 8
    axes[1].imshow(
        wheel_k8,
        cmap="gray",
        origin="upper",
        vmin=0,
        vmax=255
    )

    axes[1].set_title(
        "Wheel - k = 8"
    )

    axes[1].axis("off")


    plt.suptitle(
        f"Part 3.3 - Wheel ({wedge_count} wedges)"
    )

    plt.tight_layout()

    plt.show()
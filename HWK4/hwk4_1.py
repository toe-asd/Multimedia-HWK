import os
import sys
import numpy as np
import matplotlib.pyplot as plt
current_dir = os.path.dirname(os.path.abspath(__file__))
hwk_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(hwk_dir)

from HWK2.hwk2_1 import scanline_fill



def composite_shape(background, mask, color, alpha):
    result = background.copy()
    inside = mask > 0

    result[inside] = alpha * color + (1 - alpha) * result[inside]

    return result


width = 500
height = 500

shape_a = [
    (80, 100),
    (300, 100),
    (300, 350),
    (80, 350)
]

shape_b = [
    (190, 180),
    (420, 180),
    (420, 410),
    (190, 410)
]

# Rasterize

mask_a = scanline_fill([shape_a], width, height)
mask_b = scanline_fill([shape_b], width, height)

# Colors and transparency


color_a = np.array([255.0, 0.0, 0.0])   
color_b = np.array([0.0, 0.0, 255.0])
alpha_a = 0.5
alpha_b = 0.5

# White background


background = np.ones((height, width, 3), dtype=float) * 255.0

# Case 1: A over B
# First B, then A

result_ab = background.copy()
result_ab = composite_shape(result_ab, mask_b, color_b, alpha_b)
result_ab = composite_shape(result_ab, mask_a, color_a, alpha_a)


# Case 2: B over A
# First A, then B

result_ba = background.copy()
result_ba = composite_shape(result_ba, mask_a, color_a, alpha_a)
result_ba = composite_shape(result_ba, mask_b, color_b, alpha_b)

# Find difference

difference = np.abs(result_ab - result_ba)

# RGB 任一 channel 不同，就代表這個 pixel 有改變
changed_mask = np.any(difference > 0, axis=2)

changed_pixels = np.count_nonzero(changed_mask)

# Find overlap

overlap_mask = (mask_a > 0) & (mask_b > 0)
overlap_pixels = np.count_nonzero(overlap_mask)


# Print results
print("Changed pixels:", changed_pixels)
print("Overlap pixels:", overlap_pixels)

same_region = np.array_equal(changed_mask, overlap_mask)

print("Changed region equals overlap region:", same_region)


# Find bounding box of changed pixels

positions = np.argwhere(changed_mask)

if len(positions) > 0:
    y_min = positions[:, 0].min()
    y_max = positions[:, 0].max()

    x_min = positions[:, 1].min()
    x_max = positions[:, 1].max()

    print("Changed pixel region:")
    print("x =", x_min, "to", x_max)
    print("y =", y_min, "to", y_max)


# Check one pixel inside overlap
test_x = 250
test_y = 250

print("\nTest pixel:", (test_x, test_y))
print("A over B:", result_ab[test_y, test_x])
print("B over A:", result_ba[test_y, test_x])
# Display A over B

plt.figure()
plt.imshow(np.clip(result_ab, 0, 255).astype(np.uint8))
plt.title("A over B")
plt.axis("off")

# Display B over A

plt.figure()
plt.imshow(np.clip(result_ba, 0, 255).astype(np.uint8))
plt.title("B over A")
plt.axis("off")

# Display changed pixels

plt.figure()
plt.imshow(changed_mask, cmap="gray")
plt.title("Changed Pixels")
plt.axis("off")

plt.show()
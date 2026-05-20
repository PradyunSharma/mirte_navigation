import cv2
import numpy as np
import yaml
import os

here = os.path.dirname(os.path.abspath(__file__))
map_path = os.path.join(here, "my_map")

# Read resolution from yaml
with open(map_path + ".yaml") as f:
    meta = yaml.safe_load(f)
res = meta["resolution"]

# Read map
img = cv2.imread(map_path + ".pgm", cv2.IMREAD_GRAYSCALE)

# Binarize occupied cells
occ = (img < 50).astype(np.uint8) * 255

# Close small gaps
kernel = np.ones((3, 3), np.uint8)
occ = cv2.morphologyEx(occ, cv2.MORPH_CLOSE, kernel)

# Connected components
n, labels, stats, centroids = cv2.connectedComponentsWithStats(occ, connectivity=8)

print(f"Resolution: {res} m/pixel")
print(f"Found {n-1} components total\n")

# Filter: keep only obstacles with area in [0.15, 0.25] m^2
real_obstacles = []
for i in range(1, n):
    x, y, w, h, area = stats[i]
    area_m2 = area * res * res
    if 0.10 <= area_m2 <= 0.30:
        real_obstacles.append((i, x, y, w, h, area_m2, centroids[i]))

print(f"Obstacles with area in [0.15, 0.25] m²: {len(real_obstacles)}\n")
for idx, (i, x, y, w, h, area_m2, c) in enumerate(real_obstacles, 1):
    print(f"#{idx} (label {i}): "
          f"size {w*res:.2f} x {h*res:.2f} m, "
          f"area {area_m2:.3f} m², "
          f"center ({c[0]:.0f},{c[1]:.0f})")

# Visualize only the filtered obstacles
vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
for idx, (i, x, y, w, h, area_m2, c) in enumerate(real_obstacles, 1):
    cv2.rectangle(vis, (x, y), (x+w, y+h), (0, 0, 255), 1)
    cv2.putText(vis, str(idx), (x, y-2),
                cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)
cv2.imwrite(map_path + "_annotated.png", vis)
print(f"\nAnnotated image saved to {map_path}_annotated.png")

from return_long_lat_grid import return_long_lat_grid
from lookup_rgb_values_for_long_lat_grid import lookup_rgb_values_for_long_lat_grid
import numpy as np

path_to_tile = "data/tiles/tiled_image.103.tif"

grid = return_long_lat_grid(path_to_tile)
print(grid.shape)
grid_top = grid[:, -10:, 3000:]
print(grid_top[:, -4:, -4:], grid_top.shape)
mask = lookup_rgb_values_for_long_lat_grid(grid_top)
print(mask[:, -4:, -4:], mask.shape)


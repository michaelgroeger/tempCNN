from multiprocessing import Pool
from multiprocessing import freeze_support
from return_long_lat_grid import return_long_lat_grid
from lookup_rgb_values_for_long_lat_grid import lookup_rgb_values_for_long_lat_grid
import os
import time
from PIL import Image
import re

start = time.time()

# set number of CPUs to run on
ncore = "1"

# set env variables
# have to set these before importing numpy
os.environ["OMP_NUM_THREADS"] = ncore
os.environ["OPENBLAS_NUM_THREADS"] = ncore
os.environ["MKL_NUM_THREADS"] = ncore
os.environ["VECLIB_MAXIMUM_THREADS"] = ncore
os.environ["NUMEXPR_NUM_THREADS"] = ncore


import numpy as np

if __name__ == "__main__":
    # path_to_tile = os.path.join(
    #     "'/Volumes/Volume/QGIS/tiled_image/tiled_image." + str(105) + ".tif"
    # )
    path_to_tile = "data/tiles/tiled_image.105.tif"
    # Generate data to worked on
    # path_to_tile = os.path.join(
    # "'/Volumes/Volume/QGIS/tiled_image/tiled_image." + str(1) + ".tif"
    # )
    long_lat_grid = return_long_lat_grid(path_to_tile)
    print("Long_latgrid shape", long_lat_grid.shape)
    ####
    # Shift that separation back to column wise because now the last process
    # needs to do the entire rest after 3120
    ####
    # Intervals only for documentation reasons
    # intervals = [
    #     458,
    #     916,
    #     1374,
    #     1832,
    #     2290,
    #     2748,
    #     3206,
    #     3664,
    #     4122,
    #     4580,
    #     5038,
    #     5496,
    #     5954,
    #     6412,
    #     6870,
    #     7328,
    # ]

    data = [
        long_lat_grid[:, :, 0:458],
        long_lat_grid[:, :, 458:916],
        long_lat_grid[:, :, 916:1374],
        long_lat_grid[:, :, 1374:1832],
        long_lat_grid[:, :, 1832:2290],
        long_lat_grid[:, :, 2290:2748],
        long_lat_grid[:, :, 2748:3206],
        long_lat_grid[:, :, 3206:3664],
        long_lat_grid[:, :, 3664:4122],
        long_lat_grid[:, :, 4122:4580],
        long_lat_grid[:, :, 4580:5496],
        long_lat_grid[:, :, 5496:5954],
        long_lat_grid[:, :, 5954:6412],
        long_lat_grid[:, :, 6412:6870],
        long_lat_grid[:, :, 6870:7328],
        long_lat_grid[:, :, 7328:],
    ]
    # get max number of processes
    p = Pool(processes=16)
    # apply function to data
    result = p.map(lookup_rgb_values_for_long_lat_grid, data)
    # concatenate results
    mask = np.concatenate(
        (
            result[0],
            result[1],
            result[2],
            result[3],
            result[4],
            result[5],
            result[6],
            result[7],
            result[8],
            result[9],
            result[10],
            result[11],
            result[12],
            result[13],
            result[14],
            result[15],
        ),
        axis=2,
    )
    mask = mask.astype(np.uint8)
    print(f"Shape of mask: ", mask.shape)
    # Extract channels
    r = mask[0, :, :]
    g = mask[1, :, :]
    b = mask[2, :, :]
    # Stack channels into [H, W, C]
    rgb = np.stack([r, g, b], axis=2)
    p.close()
    p.join()
    # generate & export mask
    rgb_mask = Image.fromarray(rgb, "RGB")
    path_to_tile = re.split(r"/", path_to_tile)
    tilename = path_to_tile[-1]
    path_to_mask = os.path.join(
        "data/tiles"
        + "/"
        + "masks/new_metadata_row_iter/"
        + "mask_"
        + tilename
        + ".png"
    )
    rgb_mask.save(path_to_mask, quality=100, subsampling=0)
end = time.time()
print("The time of execution of above program is :", (end - start) / 60, " Minutes")


# smaller sample for debugging
# data = [
#     long_lat_grid[:, 0:10, 0:100],
#     long_lat_grid[:, 10:20, 0:100],
#     long_lat_grid[:, 20:30, 0:100],
#     long_lat_grid[:, 30:40, 0:100],
#     long_lat_grid[:, 40:50, 0:100],
#     long_lat_grid[:, 50:60, 0:100],
#     long_lat_grid[:, 60:70, 0:100],
#     long_lat_grid[:, 70:80, 0:100],
#     long_lat_grid[:, 80:90, 0:100],
#     long_lat_grid[:, 90:100, 0:100],
#     long_lat_grid[:, 100:110, 0:100],
#     long_lat_grid[:, 110:120, 0:100],
#     long_lat_grid[:, 120:130, 0:100],
#     long_lat_grid[:, 130:140, 0:100],
#     long_lat_grid[:, 140:150, 0:100],
#     long_lat_grid[:, 150:160, 0:100],
# ]


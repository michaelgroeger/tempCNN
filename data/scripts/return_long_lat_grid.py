import numpy as np
import json
import re


def return_long_lat_grid(path_to_metadata, path_to_tile):
    # Read in json with metadata
    with open(path_to_metadata, "r") as metadata:
        data = metadata.read()
    data = json.loads(data)

    # get correct metadata
    # find tilename to match metadata against
    tile_name = re.split(r"/", path_to_tile)
    tile_name = tile_name[-1]
    for tile in data["tiff"]:
        if tile["name"] == tile_name:
            upper_left_corner = tile["upper_left_corner"]
            lower_right_corner = tile["lower_right_corner"]
            resolution_x = tile["width"]
            resolution_y = tile["height"]
            break
    # Get corner lat & long values
    x_min, y_min = upper_left_corner[0], upper_left_corner[1]
    x_max, y_max = lower_right_corner[0], lower_right_corner[1]
    gap_x_dimension = x_max - x_min
    gap_y_dimension = y_max - y_min

    # get steps
    steps_x = gap_x_dimension / resolution_x
    steps_y = gap_y_dimension / resolution_y

    # Create 2D numpy array with interpolated values. Mind that x_max is exclusive. That might cause problems down the road.
    long_mask, lat_mask = np.mgrid[y_min:y_max:steps_y, x_min:x_max:steps_x]
    # Next, merge two masks into 2D array, lookup rgb value for each pixel and then put this value into 3D array
    # stack arrays
    stacked_array = np.stack((lat_mask, long_mask))
    return stacked_array

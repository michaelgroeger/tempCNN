import numpy as np
import pandas as pd
import json
import re
from tqdm import tqdm
from PIL import Image


def create_mask_for_tile(path_to_metadata, path_to_tile, path_to_temperature_csv):
    # Read in json with metadata
    with open(path_to_metadata, "r") as metadata:
        data = metadata.read()
    data = json.loads(data)

    # read in temperature csv
    temperature_data = pd.read_csv(path_to_temperature_csv)

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

    # Create 2D numpy array with interpolated values
    lat_mask, long_mask = np.mgrid[x_min:x_max:steps_x, y_min:y_max:steps_y]

    # Next, merge two masks into 2D array, lookup rgb value for each pixel and then put this value into 3D array
    # stack arrays
    stacked_array = np.stack((lat_mask, long_mask))
    # create mask_array
    mask = np.zeros((3, resolution_x, resolution_y))
    # Fill pixels
    for row in tqdm(range(stacked_array.shape[1]), desc="Checking rows..."):
        current_latitude = stacked_array[0, row, 0]
        # look up latitude in temperature csv
        closest_latitude_temperature = min(
            temperature_data["latitude"], key=lambda x: abs(x - current_latitude)
        )
        # filter data for only relevant rows
        relevant_temperature_data = temperature_data[
            temperature_data["latitude"] == closest_latitude_temperature
        ]
        for column in tqdm(range(stacked_array.shape[-1])):
            current_longitude = stacked_array[1, row, column]
            # look up longitude in temperature csv
            closest_longitude_temperature = min(
                relevant_temperature_data["longitude"],
                key=lambda x: abs(x - current_longitude),
            )
            # get row that matches with closes longitude and latitude
            coordinate_match = relevant_temperature_data[
                relevant_temperature_data["longitude"] == closest_longitude_temperature
            ].reset_index()
            # get RGB value from temperature data
            r = coordinate_match["R"].astype("uint8")
            g = coordinate_match["G"].astype("uint8")
            b = coordinate_match["B"].astype("uint8")

            # fill mask with new value
            mask[0, row, column] = r
            mask[1, row, column] = g
            mask[2, row, column] = b

    # export mask
    mask = mask.astype("uint8")
    rgb_mask = Image.fromarray(mask, "RGB")
    path_to_tile = re.split(r"/", path_to_tile)
    path_to_mask = os.path.join(
        path_to_tile[0:2] + "/" + "mask/" + "mask_" + tile_name + ".png"
    )
    rgb_mask.save(path_to_mask, quality=100, subsampling=0)


create_mask_for_tile(
    "data/outputs/meatadata.json",
    "data/tiles/tiled_image.0.tif",
    "data/outputs/average_temp_color_coded.csv",
)


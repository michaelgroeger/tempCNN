import numpy as np
import pandas as pd
from tqdm import tqdm


def lookup_rgb_values_for_long_lat_grid(
    stacked_array, path_to_temperature_csv="data/outputs/average_temp_color_coded.csv"
):
    # read in temperature csv
    temperature_data = pd.read_csv(path_to_temperature_csv)
    # create mask_array
    mask = np.zeros((3, stacked_array.shape[1], stacked_array.shape[2]))
    # Fill pixels
    # get steps by which we'll look up values to speed up computation
    column_steps = [i * 100 for i in range(round(stacked_array.shape[-1] / 100))]
    for row in tqdm(range(stacked_array.shape[1]), desc=f"Looking up RGB value.."):
        current_latitude = stacked_array[0, row, 0]
        # look up latitude in temperature csv
        closest_latitude_temperature = min(
            temperature_data["latitude"], key=lambda x: abs(x - current_latitude)
        )
        # filter data for only relevant rows
        relevant_temperature_data = temperature_data[
            temperature_data["latitude"] == closest_latitude_temperature
        ]
        for step in range(len(column_steps)):
            if step != len(column_steps) - 1:
                current_longitude = stacked_array[1, row, step]
                # look up longitude in temperature csv
                closest_longitude_temperature = min(
                    relevant_temperature_data["longitude"],
                    key=lambda x: abs(x - current_longitude),
                )
                coordinate_match = relevant_temperature_data[
                    relevant_temperature_data["longitude"]
                    == closest_longitude_temperature
                ].reset_index()
                r = coordinate_match["R"].astype("uint8")
                g = coordinate_match["G"].astype("uint8")
                b = coordinate_match["B"].astype("uint8")
                # fill mask with new value
                mask[0, row, column_steps[step] : column_steps[step + 1]] = r
                mask[1, row, column_steps[step] : column_steps[step + 1]] = g
                mask[2, row, column_steps[step] : column_steps[step + 1]] = b
            else:
                current_longitude = stacked_array[1, row, step]
                # look up longitude in temperature csv
                closest_longitude_temperature = min(
                    relevant_temperature_data["longitude"],
                    key=lambda x: abs(x - current_longitude),
                )
                coordinate_match = relevant_temperature_data[
                    relevant_temperature_data["longitude"]
                    == closest_longitude_temperature
                ].reset_index()
                r = coordinate_match["R"].astype("uint8")
                g = coordinate_match["G"].astype("uint8")
                b = coordinate_match["B"].astype("uint8")
                # fill mask with new value
                mask[0, row, column_steps[step] :] = r
                mask[1, row, column_steps[step] :] = g
                mask[2, row, column_steps[step] :] = b

    # return mask
    return mask


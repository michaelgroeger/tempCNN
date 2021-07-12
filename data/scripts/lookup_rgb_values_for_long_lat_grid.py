import numpy as np
import pandas as pd
from tqdm import tqdm


def lookup_rgb_values_for_long_lat_grid(
    stacked_array,
    path_to_temperature_csv="data/outputs/average_temp_color_coded.csv",
    queries=100,
):
    # read in temperature csv
    temperature_data = pd.read_csv(path_to_temperature_csv)
    # create mask_array
    mask = np.zeros((3, stacked_array.shape[1], stacked_array.shape[2]))
    # Fill pixels
    # get steps by which we'll look up values to speed up computation
    column_steps = [
        i * queries for i in range(round(stacked_array.shape[-1] / queries))
    ]
    counter = 0
    for row in tqdm(range(stacked_array.shape[1]), desc=f"Looking up RGB value.."):
        current_longitude = stacked_array[1, row, 0]
        # look up longitude in temperature csv
        closest_longitude_temperature = min(
            temperature_data["longitude"], key=lambda x: abs(x - current_longitude)
        )
        # filter data for only relevant rows
        relevant_temperature_data = temperature_data[
            temperature_data["longitude"] == closest_longitude_temperature
        ]
        for step in range(len(column_steps)):
            if step != len(column_steps) - 1:
                current_latitude = stacked_array[0, row, step]
                # look up latitude in temperature csv
                closest_latitude_temperature = min(
                    relevant_temperature_data["latitude"],
                    key=lambda x: abs(x - current_latitude),
                )
                coordinate_match = relevant_temperature_data[
                    relevant_temperature_data["latitude"]
                    == closest_latitude_temperature
                ].reset_index()
                r = coordinate_match["R"].astype("uint8")
                g = coordinate_match["G"].astype("uint8")
                b = coordinate_match["B"].astype("uint8")
                # fill mask with new value
                mask[0, row, column_steps[step] : column_steps[step + 1]] = r
                mask[1, row, column_steps[step] : column_steps[step + 1]] = g
                mask[2, row, column_steps[step] : column_steps[step + 1]] = b
                # counter += 1
                # if counter % 300 == 0:
                # print(
                #     f"Row: {row}, step: {step}, Lat: {current_latitude}, Long: {current_longitude}, R: {int(r)}, G: {int(g)}, B: {int(b)},"
                # )
            else:
                current_latitude = stacked_array[0, row, step]
                # look up latitude in temperature csv
                closest_latitude_temperature = min(
                    relevant_temperature_data["latitude"],
                    key=lambda x: abs(x - current_latitude),
                )
                coordinate_match = relevant_temperature_data[
                    relevant_temperature_data["latitude"]
                    == closest_latitude_temperature
                ].reset_index()
                r = coordinate_match["R"].astype("uint8")
                g = coordinate_match["G"].astype("uint8")
                b = coordinate_match["B"].astype("uint8")
                # fill mask with new value
                mask[0, row, column_steps[step] :] = r
                mask[1, row, column_steps[step] :] = g
                mask[2, row, column_steps[step] :] = b
                # print(
                #     f"Row: {row}, step: {step}, Lat: {current_latitude}, Long: {current_longitude}, R: {int(r)}, G: {int(g)}, B: {int(b)},"
                # )
    # return mask
    return mask


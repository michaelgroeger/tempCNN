from PIL import Image
import numpy as np
import json
from read_image_into_array import load_image
import os

# read json
def stitch_masks(path_to_metadata, latitude, path_to_masks="data/tiles/masks"):
    # Read in json with metadata
    with open(path_to_metadata, "r") as metadata:
        data = metadata.read()
    data = json.loads(data)

    # get all tiles belonging to a certain row of tiles
    tile_row = []
    # Extract all longitudes of the matching tiles to bring the in the correct order
    longitudes = []
    heights = []
    widths = []
    for tile in data["tiff"]:
        # Collect all tiles belonging to a row of tiles by getting all the ones that share the same
        # latitude in the upper left corner
        if tile["upper_left_corner"][1] == latitude:
            tile_row.append(tile)
            longitudes.append(tile["upper_left_corner"][0])
            heights.append(tile["height"])
            widths.append(tile["width"])

    # Put tiles in increasing order
    longitudes.sort()
    # Get extend of stitched mask
    x_resolution = 0
    y_resolution = list(set(heights))[0]
    for tile in tile_row:
        # We don't need to add the height because the tiles are stitched row wise
        x_resolution += tile["width"]

    # import & hstack masks
    ordered_masks = []
    # Debug missing zero mask
    longitudes.pop(0)
    for longitude in longitudes:
        for tile in tile_row:
            if tile["upper_left_corner"][0] == longitude:
                # build path to mask
                path_to_mask = os.path.join(
                    path_to_masks, "mask_" + tile["name"] + ".png"
                )
                # load image into numpy array
                mask = load_image(path_to_mask)
                print(tile["name"], " : ", {mask.shape})
                ordered_masks.append(mask)

    # Get first mask
    first_mask = ordered_masks.pop(0)
    first_mask = ordered_masks.pop(0)
    for mask in ordered_masks:
        print(mask.shape)
        # first_mask = np.hstack((first_mask, mask))

    # print(
    #     x_resolution,
    #     y_resolution,
    #     list(set(widths)),
    #     list(set(heights)),
    #     len(tile_row),
    #     first_mask.shape,
    # )


stitch_masks("data/outputs/meatadata.json", 49.41004772748967)


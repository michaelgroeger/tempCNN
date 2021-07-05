from osgeo import gdal
from os import listdir
from os.path import isfile, join
from tqdm import tqdm
import json

ds = gdal.Open("data/tiles/tiled_image.0.tif")
width = ds.RasterXSize
height = ds.RasterYSize
gt = ds.GetGeoTransform()
minx = gt[0]
miny = gt[3] + width * gt[4] + height * gt[5]
maxx = gt[0] + width * gt[1] + height * gt[2]
maxy = gt[3]


def create_tile_metadata(path_to_tiles, path_output_json):
    # Get number of files in directory
    tiff_files = [f for f in listdir(path_to_tiles) if isfile(join(path_to_tiles, f))]
    metadata = {"tiff": []}
    for tiff in tqdm(range(len(tiff_files)), desc="Collecting metadata "):
        # Open tiff file
        ds = gdal.Open(path_to_tiles + "/" + tiff_files[tiff])
        # Get Metadata
        width = ds.RasterXSize
        height = ds.RasterYSize
        gt = ds.GetGeoTransform()
        minx = gt[0]
        miny = gt[3] + width * gt[4] + height * gt[5]
        maxx = gt[0] + width * gt[1] + height * gt[2]
        maxy = gt[3]
        # Create json
        metadata["tiff"].append(
            {
                "index": tiff,
                "name": tiff_files[tiff],
                "upper_left_corner": [minx, miny],
                "upper_right_corner": [maxx, maxy],
            }
        )

    with open(path_output_json, "w") as fp:
        json.dump(metadata, fp)


create_tile_metadata("data/tiles", "data/outputs/meatadata.json")


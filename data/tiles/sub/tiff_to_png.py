import os
from PIL import Image

im = Image.open("data/tiles/tiled_image.0.tif")
im.thumbnail(im.size)
im.save("data/tiles/sub/test_big_02.png", quality=100, subsampling=0)


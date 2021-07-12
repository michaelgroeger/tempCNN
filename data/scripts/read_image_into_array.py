from PIL import Image
import numpy as np


def load_image(infilename):
    img = Image.open(infilename)
    img.load()
    data = np.asarray(img, dtype="uint8")
    return data

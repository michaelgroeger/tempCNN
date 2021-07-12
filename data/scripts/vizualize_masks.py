from PIL import Image
import re
import os


def visualize_mask(image_path, mask_path):
    # Ground truth image
    background = Image.open(image_path)
    # Generate path to mask
    image_path = re.split(r"/", image_path)
    # path_to_mask = os.path.join(
    #     image_path[0] + "/" + image_path[1] + "/" + image_path[2] + "_masks"
    #     "/" + "mask_" + image_path[-1]
    # ).replace(".jpg", ".png")
    path_to_mask = mask_path
    # load mask
    overlay = Image.open(path_to_mask)
    # Ensure same encoding
    background = background.convert("RGBA")
    overlay = overlay.convert("RGBA")
    # Create new image from overlap and make overlay 50 % transparent
    new_img = Image.blend(background, overlay, 0.5)
    new_img.show()


visualize_mask(
    "data/tiles/tiled_image.103.tif",
    "data/tiles/masks/tests/new_metadata_row_iter/mask_tiled_image.103.tif.png",
)
## Source:
# https://stackoverflow.com/questions/10640114/overlay-two-same-sized-images-in-python/44749818


import numpy as np
from PIL import Image as im

def slice(img_arr, channel, bit_index):
    height, width, z = img_arr.shape

    new_image = im.new('1', (width, height))
    new_image_data = new_image.load()

    for x in range(height):
        for y in range(width):
            new_image_data[y,x]=int(f'{img_arr[x,y,channel]:08b}'[bit_index])*255

    return new_image
img = im.open(r"test/bitplane.png", "r")
img_arr = np.array(img)

for channel in range(4):
    for bit_index in range(8):
        new_image = slice(img_arr, channel, bit_index)
        new_image.save(r"test/bitplane/{}{}.png".format("RGBA"[channel], bit_index))

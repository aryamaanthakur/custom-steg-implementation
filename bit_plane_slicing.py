import numpy as np
from PIL import Image as im
import multiprocessing 
import time

def slice(img_arr, channel, bit_index):
    height, width, z = img_arr.shape

    new_image = im.new('1', (width, height))
    new_image_data = new_image.load()
    
    for x in range(height):
        for y in range(width):
            try:
                new_image_data[y,x]=int(f'{img_arr[x,y,channel]:08b}'[bit_index])*255
            except IndexError:
                pass

    new_image.save(r"test/bitplane/{}{}.png".format("RGBA"[channel], bit_index))
    print("[+] {}{} Done!".format("RGBA"[channel], bit_index))

if __name__ == "__main__": 
    img = im.open(r"test/bitplane.png", "r")
    img_arr = np.array(img)

    print(img_arr.shape)
    t1 = time.time()
    if img.mode == "RGBA": n=4
    elif img.mode == "RGB": n=3


    for channel in range(n):
        threads = []
        for bit_index in range(8):
            threads.append(multiprocessing.Process(target=slice, args=(img_arr, channel, bit_index)))
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
            
    t2 = time.time()
    print("Time taken for execution with threading", t2-t1, "seconds")

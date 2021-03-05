import numpy as np
from PIL import Image as im
import multiprocessing 
#import threading
import time

#NOTE: using class didn't work

""" class ThreadSolver(threading.Thread):
    def __init__(self, img_arr, channel, bit_index):
        threading.Thread.__init__(self)
        self.channel = channel
        self.bit_index = bit_index
        self.img_arr = img_arr

    def run(self):
        slice(self.img_arr, self.channel, self.bit_index) """

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

def analyse(location):
    img = im.open(location, "r")
    
    img_arr = np.array(img)
    print(img_arr.shape)

    if img.mode == "RGBA": n=4
    elif img.mode == "RGB": n=3
    
    processes = []

    for channel in range(n):
        for bit_index in range(8):
            processes.append(multiprocessing.Process(target=slice, args=(img_arr, channel, bit_index)))
        
    for process in processes:
        process.start()

    for process in processes:
        process.join()

    """ threads = []
    for channel in range(n):
        for bit_index in range(8):
            thread = ThreadSolver(img_arr, channel, bit_index)
            thread.start()
            threads.append(thread)
    
    for thread in threads:
        thread.join() """

if __name__ == "__main__":
    location = r"test/bitplane.png"

    t1 = time.time()  
    analyse(location)
    t2 = time.time()
    print("Time taken for execution with multiprocessing", t2-t1, "seconds")

import numpy as np
from PIL import Image as im
import math

def hide(img, msg, msg_end="#steg-end#"):
    width, height = img.size
    msg+=msg_end
    msg_bin = "".join([f'{ord(i):08b}' for i in msg]) #converting ascii message to 8bit binary form
    msg_len = len(msg_bin)
    img_array = np.array(list(img.getdata())) #image as a continuous array of pixels
    if img.mode == "RGB": n = 3
    elif img.mode == "RGBA": n = 4
    else:
        print("Invalid image mode")
        return None

    max_lsb = width*height*n

    #checking if image has sufficient pixels to hide data
    if (msg_len > max_lsb):
        print("Image not large enough to hide data")
        return None
    
    index = 0
    for i in range(math.ceil(msg_len/4)):
        for j in range(n):
            img_array[i][j] = int(bin(img_array[i][j])[2:-1] + msg_bin[index], 2)
            index+=1
    
    img_array=img_array.reshape(height, width, n)
    new_img = im.fromarray(img_array.astype('uint8'), img.mode)
    print("Image Encoded Successfully")
    return new_img

#img = im.open("test.png", "r")
#new_img = hide(img, "Hello World")
#new_img.save("test0.png")



def unhide(img, msg_end="#steg-end#"):
    
    img_array = np.array(list(img.getdata())) #image as a continuous array of pixels
    if img.mode == "RGB": n = 3
    elif img.mode == "RGBA": n = 4
    else:
        print("Invalid image mode")
        return None
    
    hidden_msg = ""
    for i in range(img_array.shape[0]):
        for j in range(n):
            hidden_msg += bin(img_array[i][j])[-1]
    ascii_msg = ""
    for i in range(0, len(hidden_msg), 8):
        ascii_msg += chr(int(hidden_msg[i:i+8], 2))
        if ascii_msg[-len(msg_end):]==msg_end: break
    
    return ascii_msg[:-len(msg_end)]

img = im.open("test0.png", "r")
msg = unhide(img)
print(msg)
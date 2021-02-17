import numpy as np
from PIL import Image as im
import math
from itertools import permutations

def bin_to_ascii(bin_msg):
    ascii_msg = ""
    for i in range(0, len(bin_msg), 8):
        ascii_msg += chr(int(bin_msg[i:i+8], 2))

    return ascii_msg

def hide(img, msg, msg_end="#steg-end#"):
    width, height = img.size
    msg+=msg_end #using a string to determine the end of message while decoding
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
    for i in range(msg_len):
        for j in range(n):
            img_array[i][j] = int(bin(img_array[i][j])[2:-1] + msg_bin[index], 2)
            index+=1
        if index==msg_len: break

    img_array=img_array.reshape(height, width, n)
    new_img = im.fromarray(img_array.astype('uint8'), img.mode)
    print("Image Encoded Successfully")
    return new_img

img = im.open("test/test.png", "r")
new_img = hide(img, r"gunnHacks{abcdefgasdmfalsjdflaskjdflkdf}")
new_img.save("test/test0.png")


def extract(img_arr, channel_order, bit_start, bit_end, msg_len):
    hidden_msg = ""
    height, width, z = img_arr.shape
    c = 0
    for x in range(height):
        for y in range(width):
            for z in channel_order:
                hidden_msg += f'{img_arr[x,y,z]:08b}'[bit_start:bit_end]
                c+=1
                if c==msg_len: return hidden_msg
    return hidden_msg

def analyse(img, bit_start, bit_end, msg_len=400, search=""):
    img_arr = np.array(img)

    channel_orders = []
    if img.mode=="RGBA":
        for i in range(1,5):
	        for j in permutations("RGBA", i):
		        channel_orders.append("".join(j))
    elif img.mode=="RGB":
        for i in range(1,4):
	        for j in permutations("RGB", i):
		        channel_orders.append("".join(j))
    else:
        print("Invalid Image Mode")
        return None

    if bit_end-bit_start==1: print("[=] Checking bit number", bit_start+1, "\n")
    else: print("[=] Checking from bit", bit_start+1, "to", bit_end, "\n")

    for test in channel_orders:
        channel_order = [img.mode.index(channel) for channel in test]
        bin_msg = extract(img_arr, channel_order, bit_start, bit_end, msg_len)
        ascii_msg = bin_to_ascii(bin_msg)
        if search in ascii_msg:
            print("[+]", test, "-", ascii_msg)

img = im.open("test/test0.png", "r")
img_arr = np.array(img)
bin_msg = extract(img_arr, [0,1,2,3], 7, 8, 500)
#print(bin_to_ascii(bin_msg))

analyse(img, 7, 8)

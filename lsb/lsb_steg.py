import numpy as np
from PIL import Image as im
from itertools import permutations

def bin_to_ascii(bin_msg):
    ascii_msg = bytearray()
    for i in range(0, len(bin_msg), 8):
        x = int(bin_msg[i:i+8], 2)
        ascii_msg.append(x)
        """ if x in range(30,127):
            ascii_msg.append(x)
        else:
            ascii_msg.append(63) """

    return ascii_msg

def ascii_to_bin(ascii_msg):
    bin_msg = ""
    for i in ascii_msg:
        bin_msg+=f'{ord(i):08b}'

    return bin_msg

def hide(img, img_arr, channel_order, bit_start, bit_end, msg):

    msg = ascii_to_bin(msg)
    msg_len = len(msg)

    height, width, z = img_arr.shape

    max_msg_len = height*width*len(channel_order)*(bit_end-bit_start)

    if max_msg_len < msg_len:
        print("[-] Image not large enough to hide message in given channel order")
        return None
    
    bit_len = bit_end-bit_start
    index = 0
    for x in range(height):
        for y in range(width):
            for z in channel_order:
                curr_value = f'{img_arr[x,y,z]:08b}'
                if bit_end==8:
                    new_value = curr_value[0:bit_start]+msg[index:index+bit_len]
                else:
                    new_value = curr_value[0:bit_start]+msg[index:index+bit_len]+curr_value[bit_end:]

                img_arr[x,y,z] = int(new_value,2)
                index+=bit_len
                
                if index>=msg_len:
                    new_img = im.fromarray(img_arr.astype('uint8'), img.mode)
                    print("Image Encoded Successfully")
                    return new_img

    return new_img
    

img = im.open("test/test.png", "r")

if img.mode == "RGBA" or img.mode == "RGB":
    img_arr = np.array(img)
    new_img = hide(img, img_arr, [2,1,0], 6, 8, "Hello hello hello, What up?")
    new_img.save("test/test0.png")
else:
    print("[-] Invalid image mode! Please use an RGB/RGBA image")


def extract(img_arr, channel_order, bit_start, bit_end, msg_len):
    hidden_msg = "" #make by
    height, width, z = img_arr.shape
    bit_len=bit_end-bit_start
    c = 0
    for x in range(height):
        for y in range(width):
            for z in channel_order:
                hidden_msg += f'{img_arr[x,y,z]:08b}'[bit_start:bit_end]
                c+=bit_len
                if c>=msg_len: return hidden_msg

    return hidden_msg

def check_readability(b_string, min_readable_characters=5):
    max_readable_characters = 0
    current_max = 0

    for i in b_string:
        if i in range(30,127):
            current_max+=1
        else:
            if max_readable_characters < current_max:
                max_readable_characters = current_max

    if max_readable_characters >= min_readable_characters:
        return True
    else:
        return False

def analyse(img, bit_start, bit_end, msg_len=400, search=b"", min_readable_characters=0):
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

    if bit_end-bit_start==1:
        print("[=] Checking bit number", bit_start+1, "\n")
    else:
        print("[=] Checking from bit", bit_start+1, "to", bit_end, "\n")

    if search!="":
        print("[=] Searching for keyword", search)

    for test in channel_orders:
        channel_order = [img.mode.index(channel) for channel in test]
        bin_msg = extract(img_arr, channel_order, bit_start, bit_end, msg_len)
        ascii_msg = bin_to_ascii(bin_msg)
        if (search in ascii_msg) and check_readability(ascii_msg, min_readable_characters):
            print("[+]", test, "-", "".join(map(chr, ascii_msg)))
            #print("[+]", test, "-", ascii_msg)
img = im.open("test/test0.png", "r")
img_arr = np.array(img)
#bin_msg = extract(img_arr, [0,1,2], 7, 8, 500)
#print(bin_to_ascii(bin_msg))

analyse(img, 6, 8, 500, b"", 20)

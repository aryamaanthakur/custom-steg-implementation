import numpy as np
from PIL import Image as im

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

def bin_to_ascii(bin_msg):
    ascii_msg = bytearray()
    for i in range(0, len(bin_msg), 8):
        x = int(bin_msg[i:i+8], 2)
        ascii_msg.append(x)
    return ascii_msg

def ascii_to_bin(ascii_msg):
    bin_msg = ""
    for i in ascii_msg:
        bin_msg+=f'{ord(i):08b}'

    return bin_msg

def hide(image_location, text_location, channels, bit_start, bit_end):

    files = [("PNG File", '*.png')]
    filename = filedialog.asksaveasfile(filetypes = files, defaultextension = files)
    if filename==None:
        print("[-] No location selected for saving")
        return None

    if text_location=="":
        return None

    if image_location=="":
        return None

    if bit_start>=bit_end:
        return None
    
    img = im.open(image_location)
    img_arr = np.array(img)

    for channel in channels:
        if channel not in img.mode:
            return None

    channel_order = []
    for channel in channels:
        channel_order.append(img.mode.index(channel))

    msg = open(text_location).read()
    msg = ascii_to_bin(msg)
    msg_len = len(msg)
    msg+="00000000"
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

                print(curr_value, new_value)
                img_arr[x,y,z] = int(new_value,2)
                index+=bit_len
                
                if index>=msg_len:
                    new_img = im.fromarray(img_arr.astype('uint8'), img.mode)
                    print("Image Encoded Successfully")
                    new_img.save(filename.name)
                    return None

    return None

def openimage():
    global image_location
    filename = filedialog.askopenfilename(title = "Open") 
    image_location = filename
    image_location_label.configure(text=image_location)

def opentext():
    global text_location
    filename = filedialog.askopenfilename(title = "Open") 
    text_location = filename
    text_location_label.configure(text=text_location)

if __name__ == "__main__":

    image_location = ""
    text_location = ""

    channel_names = ['R', 'G', 'B', 'A', 'RG', 'RB', 'RA', 'GR',
                    'GB', 'GA', 'BR', 'BG', 'BA', 'AR', 'AG', 'AB',
                    'RGB', 'RGA', 'RBG', 'RBA', 'RAG', 'RAB', 'GRB', 'GRA',
                    'GBR', 'GBA', 'GAR', 'GAB', 'BRG', 'BRA', 'BGR', 'BGA',
                    'BAR', 'BAG', 'ARG', 'ARB', 'AGR', 'AGB', 'ABR', 'ABG',
                    'RGBA', 'RGAB', 'RBGA', 'RBAG', 'RAGB', 'RABG', 'GRBA', 'GRAB',
                    'GBRA', 'GBAR', 'GARB', 'GABR', 'BRGA', 'BRAG', 'BGRA', 'BGAR',
                    'BARG', 'BAGR', 'ARGB', 'ARBG', 'AGRB', 'AGBR', 'ABRG', 'ABGR']

    bits = [1, 2, 3, 4, 5, 6, 7, 8]
    root = Tk()
    root.title("RGB Bit Plane Slicing")
    root.geometry("300x250") 
    root.resizable(width = True, height = True)

    img_btn = Button(root, text="Load Image", command=openimage).place(x=10, y=10)
    image_location_label = Label(root, text="")
    image_location_label.place(x=100, y=15)

    img_btn = Button(root, text="Load Text", command=opentext).place(x=10, y=50)
    text_location_label = Label(root, text="")
    text_location_label.place(x=100, y=55)


    channels = StringVar(root)
    channels.set(channel_names[0])
    channels_dropdown = OptionMenu(root, channels, *channel_names).place(x=100, y=90)

    bit_start = IntVar(root)
    bit_end = IntVar(root)
    
    bit_start.set(8)
    bit_end.set(8)

    bit_start_dropdown = OptionMenu(root, bit_start, *bits).place(x=70, y=130)
    bit_end_dropdown = OptionMenu(root, bit_end, *bits).place(x=70, y=170)

    channels_label = Label(root, text="Channel Order: ").place(x=10, y=95)
    bit_start_label = Label(root, text="Bit Start: ").place(x=10, y=135)
    bit_end_label = Label(root, text="Bit End: ").place(x=10, y=175)

    hide_btn = Button(root, text="Hide", command=lambda: hide(image_location, text_location, channels.get(), bit_start.get()-1, bit_end.get()))
    hide_btn.place(x=10, y=210)
    root.mainloop()
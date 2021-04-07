from hashlib import sha256
from Crypto.Cipher import AES
from PIL import Image as im
import numpy as np
import random

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext

def Encrypt(data, key):
    cipher_encrypt = AES.new(key, AES.MODE_CFB, iv=key[:16])
    ciphered_bytes = cipher_encrypt.encrypt(data)

    return ciphered_bytes

def Decrypt(ciphered_data, key):

    cipher_decrypt = AES.new(key, AES.MODE_CFB, iv=key[:16])
    deciphered_bytes = cipher_decrypt.decrypt(ciphered_data)

    return deciphered_bytes

def hide(image_location, text_location):
    
    if image_location == "":
        print("[-] Image not selected")
        return None
    
    if text_location == "":
        print("[-] Text file not selected")
        return None

    files = [("PNG File", '*.png'), ("JPG File", '*.jpg')]
    filename = filedialog.asksaveasfile(filetypes = files, defaultextension = files)
    if filename == None:
        print("[-] No location selected for saving")
        return None

    with open(text_location) as file:
        data = file.read()

    img = im.open(image_location)
    img_arr = np.array(img.getdata())
    img_len, n = img_arr.shape
    width, height = img.size

    password = password_textbox.get("1.0", "end-1c")

    key = sha256(password.encode()).digest()
    ciphered_data = Encrypt(data.encode("utf-8"), key)

    bin_msg = "".join(f'{i:08b}' for i in ciphered_data)

    msg_len = len(bin_msg)
    msg_index = 0

    random.seed(password.encode("utf-8"))
    for img_index in range(img_len):

        pixel = img_arr[img_index]

        channel_prng = random.randint(0,6)
        channel_names = [[0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2]]
        channels = channel_names[channel_prng]
    
        bits_prng = random.randint(1,3)
        bits_len = bits_prng

        current_msg_len = len(channels)*bits_len

        if msg_index+current_msg_len > msg_len:
            current_msg = bin_msg[msg_index:]+"0"*(current_msg_len - msg_len + msg_index)
        else:
            current_msg = bin_msg[msg_index:msg_index+current_msg_len]

        msg_index+=current_msg_len

        for channel in channels:
            curr_value = f'{pixel[channel]:08b}'
            new_value = curr_value[0:(8-bits_len)]+current_msg[0:bits_len]
            img_arr[img_index][channel] = new_value

            current_msg = current_msg[bits_len:]

        if msg_index>=msg_len:
            break
        
    img_arr=img_arr.reshape(height, width, n)
    new_img = im.fromarray(img_arr.astype('uint8'), img.mode)
    new_img.save(filename.name)

    print("Image Encoded Successfully")

#image_location = "test\\flag.png"
#hide(image_location, data, password)

def unhide(image_location):

    if image_location == "":
        print("[-] Image not selected")
        return None

    files = [("Text File", '*.txt')]
    filename = filedialog.asksaveasfile(filetypes = files, defaultextension = files)
    if filename == None:
        print("[-] No location selected for saving")
        return None

    img = im.open(image_location)
    img_arr = np.array(img.getdata())

    password = password_textbox.get("1.0", "end-1c")
    key = sha256(password.encode()).digest()
    
    cycles = cycles_textbox.get("1.0", "end-1c")
    if cycles == "":
        cycles = 50
    elif not cycles.isnumeric():
        return None
    else:
        cycles = int(cycles)


    msg = ""

    random.seed(password.encode("utf-8"))
    for img_index in range(cycles):

        pixel = img_arr[img_index]

        channel_prng = random.randint(0,6)
        channel_names = [[0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2]]
        channels = channel_names[channel_prng]
    
        bits_prng = random.randint(1,3)
        bits_len = bits_prng

        current_msg = ""
        for channel in channels:
            curr_value = f'{pixel[channel]:08b}'
            current_msg += curr_value[(8-bits_len):]
        
        msg+=current_msg

    ciphered_data = bytearray()
    for i in range(0, len(msg), 8):
        x = int(msg[i:i+8], 2)
        ciphered_data.append(x)

    deciphered_data = Decrypt(ciphered_data, key)

    with open(filename.name, "wb") as f:
        f.write(deciphered_data)

    print("[+] Image Decoded Successfully")
def show(image_location):

    if image_location == "":
        print("[-] Image not selected")
        return None

    img = im.open(image_location)
    img_arr = np.array(img.getdata())

    password = password_textbox.get("1.0", "end-1c")
    key = sha256(password.encode()).digest()
    
    cycles = cycles_textbox.get("1.0", "end-1c")
    if cycles == "":
        cycles = 50
    elif not cycles.isnumeric():
        return None
    else:
        cycles = int(cycles)

    msg = ""

    random.seed(password.encode("utf-8"))
    for img_index in range(cycles):

        pixel = img_arr[img_index]

        channel_prng = random.randint(0,6)
        channel_names = [[0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2]]
        channels = channel_names[channel_prng]
    
        bits_prng = random.randint(1,3)
        bits_len = bits_prng

        current_msg = ""
        for channel in channels:
            curr_value = f'{pixel[channel]:08b}'
            current_msg += curr_value[(8-bits_len):]
        
        msg+=current_msg

    ciphered_data = bytearray()
    for i in range(0, len(msg), 8):
        x = int(msg[i:i+8], 2)
        ciphered_data.append(x)

    deciphered_data = Decrypt(ciphered_data, key)
    ascii_msg = "".join(chr(i) for i in deciphered_data)

    msg_window = Toplevel(root)
    msg_window.geometry("420x300")
    txt = scrolledtext.ScrolledText(msg_window, undo=True)
    txt['font'] = ('consolas', '12')
    txt.pack(expand=True, fill='both')
    txt.insert(END,ascii_msg)
    txt.config(state=DISABLED)
    print(ascii_msg)
    msg_window.mainloop()

#unhide("test\\flag0.png", password, 45)

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

    root = Tk()
    root.title("RGB Bit Plane Slicing")
    root.geometry("300x230") 
    root.resizable(width = True, height = True)

    img_btn = Button(root, text="Load Image", command=openimage).place(x=10, y=10)
    image_location_label = Label(root, text="")
    image_location_label.place(x=100, y=15)

    txt_btn = Button(root, text="Load Text", command=opentext).place(x=10, y=50)
    text_location_label = Label(root, text="")
    text_location_label.place(x=100, y=55)

    number_of_cycles = IntVar(root)
    cycles_label = Label(root, text="Enter number of cycles to perform: ")
    cycles_label.place(x=10, y=95)
    cycles_textbox = Text(root, height=1, width=7)
    cycles_textbox.place(x=210, y=95)

    password_label = Label(root, text="Password:")
    password_label.place(x=10, y=135)
    password_textbox = Text(root, height=1, width=15)
    password_textbox.place(x=80, y=135)

    hide_btn = Button(root, text="Hide", command= lambda: hide(image_location, text_location))
    hide_btn.place(x=10, y=175)

    unhide_btn = Button(root, text="Unhide & Save", command= lambda: unhide(image_location))
    unhide_btn.place(x=60, y=175)
    
    show_btn = Button(root, text="Show", command= lambda: show(image_location))
    show_btn.place(x=160, y=175)

    root.mainloop()
import numpy as np
from PIL import Image as im

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

import os

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

    new_image.save(r"bitplane-temp/{}{}.png".format("RGBA"[channel], bit_index))
    print("[+] {}{} Done!".format("RGBA"[channel], bit_index))

def hide(host_img, secret_img, bit_plane_index):
    host_img_data = host_img.load()
    secret_img = secret_img.convert('1')
    secret_img_data = secret_img.load()
    channel = "RGBA".index(bit_plane_index[0])
    bit_index = bit_plane_index[1]

    """ for i in b_and_w_img.size[0]:
        for j in b_and_w_img.size[1]:
            new_value = f'{host_img[i,j,channel]:08b}' """

    for i in range(secret_img.size[0]):
        for j in range(secret_img.size[1]):
            pixel = host_img_data[i,j]
            new_value = f'{pixel[channel]:08b}'
            new_value = new_value[:bit_index]+str(int(secret_img_data[i,j]/255))+new_value[bit_index+1:]
            new_pixel = pixel[:channel]+(int(new_value, 2),) + pixel[channel+1:]
            host_img_data[i,j] = new_pixel
            
    return host_img

def openhostimage():
    global host_image_location
    filename = filedialog.askopenfilename(title = "Open") 
    host_image_location = filename
    host_img_label.configure(text=host_image_location)

def opensecretimage():
    global secret_image_location
    filename = filedialog.askopenfilename(title = "Open") 
    secret_image_location = filename
    secret_img_label.configure(text=secret_image_location)

def saveimage(host_image_location, secret_image_location, bit_plane_index):
    files = [("PNG File", '*.png')]
    filename = filedialog.asksaveasfile(filetypes = files, defaultextension = files)
    if filename==None:
        print("[-] No location selected for saving")
        return None
    
    if (secret_image_location==""):
        messagebox.showerror("Error", "Image to hide not selected") 
        return None
    if (host_image_location==""):
        messagebox.showerror("Error", "Host Image not selected") 
        return None

    secret_img = im.open(secret_image_location)
    host_img = im.open(host_image_location)
    
    secret_img_size = secret_img.size
    host_img_size = host_img.size

    if (secret_img_size[0]>host_img_size[0]) or (secret_img_size[1]>host_img_size[1]):
        messagebox.showerror("Error", "File size too big to hide, select a larger host image or smaller secret image") 
        return None
    
    if bit_plane_index[0] not in host_img.mode:
        messagebox.showerror("Error", "Selected plane not in host, select other plane") 
        return None
    
    img = hide(host_img, secret_img, bit_plane_index)
    img.save(filename.name)

    messagebox.showinfo("Succesful", "Secret image hidden in host successfully") 
if __name__ == "__main__":

    host_image_location = ""
    secret_image_location = ""

    bit_plane_names = ["Red-0","Red-1","Red-2","Red-3","Red-4","Red-5","Red-6","Red-7",
                       "Green-0","Green-1","Green-2","Green-3","Green-4","Green-5","Green-6","Green-7",
                       "Blue-0","Blue-1","Blue-2","Blue-3","Blue-4","Blue-5","Blue-6","Blue-7",
                       "Alpha-0","Alpha-1","Alpha-2","Alpha-3","Alpha-4","Alpha-5","Alpha-6","Alpha-7",]

    bit_plane_indices = [('R',0),('R',1),('R',2),('R',3),('R',4),('R',5),('R',6),('R',7),
                         ('G',0),('G',1),('G',2),('G',3),('G',4),('G',5),('G',6),('G',7),
                         ('B',0),('B',1),('B',2),('B',3),('B',4),('B',5),('B',6),('B',7),
                         ('A',0),('A',1),('A',2),('A',3),('A',4),('A',5),('A',6),('A',7),]

    channel_names = ["Red", "Blue", "Green", "Alpha"]
    bit_positions = [0, 1, 2, 3, 4, 5, 6, 7]

    root = Tk()
    root.title("RGB Bit Plane Hiding")
    root.geometry("400x180") 
    root.resizable(width = True, height = True)

    host_img_btn = Button(root, text ='Load Host Image', command = openhostimage).place(x=10, y=10)
    secret_img_btn = Button(root, text ='Load Image to hide', command = opensecretimage).place(x=10, y=50)

    channel = StringVar(root)
    bit_position = IntVar(root)

    channel.set(channel_names[0])
    bit_position.set(bit_positions[0])
    channel_dropdown = OptionMenu(root, channel, *channel_names).place(x=90, y=90)
    bit_position_dropdown = OptionMenu(root, bit_position, *bit_positions).place(x=280, y=90)

    channel_label = Label(root, text="Select plane:").place(x=10, y=95)
    bit_position_label = Label(root, text = "Select Bit Position:").place(x=170, y=95)
    #bit_plane_index = bit_plane_indices[bit_plane_names.index(bit_plane.get())]

    hide_button = Button(root, text="Hide", command = lambda: saveimage(host_image_location, secret_image_location, 
    (channel.get()[0], bit_position.get()))).place(x=10, y=130) #bit_plane_indices[bit_plane_names.index(bit_plane.get())]

    host_img_label = Label(root, text="")
    host_img_label.place(x=140, y=15)
    secret_img_label = Label(root, text="")
    secret_img_label.place(x=140, y=55)
    
    root.mainloop()
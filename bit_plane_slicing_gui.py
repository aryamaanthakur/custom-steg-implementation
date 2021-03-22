import glob
import numpy as np
from PIL import Image as im
from PIL import ImageTk
import multiprocessing 
#import threading
import time
from tkinter import *
from tkinter import filedialog
import os
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

    new_image.save(r"bitplane-temp/{}{}.png".format("RGBA"[channel], bit_index))
    print("[+] {}{} Done!".format("RGBA"[channel], bit_index))

def analyse():
    
    t1 = time.time()

    image_names=glob.glob('bitplane-temp\\*.png')
    for i in image_names:
        if os.path.exists(i):
            os.remove(i)

    location = openfilename()

    if location == "":
        print("[-] No file selected for performing operations")
        return None
    img = im.open(location, "r")
    width, height = img.size
    if width <= height:
        ratio = 500/height
    else:
        ratio = 600/width
    
    display_height = int(ratio*height)
    display_width = int(ratio*width)

    root.geometry("{}x{}".format(display_width+20, display_height+50))
    #print(display_width, display_height)
    img.save("bitplane-temp\\0.png")
    #tk_img = ImageTk.PhotoImage(img)
    
    img_arr = np.array(img)
    #print(img_arr.shape)

    if img.mode == "RGBA":
        n=4
        plane_names = ["Original","Alpha-0","Alpha-1","Alpha-2","Alpha-3","Alpha-4","Alpha-5","Alpha-6","Alpha-7",
                        "Blue-0","Blue-1","Blue-2","Blue-3","Blue-4","Blue-5","Blue-6","Blue-7",
                        "Green-0","Green-1","Green-2","Green-3","Green-4","Green-5","Green-6","Green-7",
                        "Red-0","Red-1","Red-2","Red-3","Red-4","Red-5","Red-6","Red-7",]
    elif img.mode == "RGB":
        n=3
        plane_names = ["Original","Blue-0","Blue-1","Blue-2","Blue-3","Blue-4","Blue-5","Blue-6","Blue-7",
                        "Green-0","Green-1","Green-2","Green-3","Green-4","Green-5","Green-6","Green-7",
                        "Red-0","Red-1","Red-2","Red-3","Red-4","Red-5","Red-6","Red-7",]
    
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

    t2 = time.time()
    print("\n[+] Time taken for completion:", t2-t1, "seconds")

    image_names=glob.glob('bitplane-temp\\*.png')
    #print(image_names)
    img = im.open(image_names[0])
    img = img.resize((display_width, display_height), im.NEAREST)
    tk_img = ImageTk.PhotoImage(img)
    panel.configure(image=tk_img)
    panel.image = tk_img
    image_name_label.configure(text=plane_names[0])
    index = 0
    def show_prev_image():
        nonlocal index
        
        index-=1
        if index == -1:
            index = len(image_names)-1
        
        img = im.open(image_names[index])
        img = img.resize((display_width, display_height), im.NEAREST)
        tk_img = ImageTk.PhotoImage(img)
        panel.configure(image=tk_img)
        panel.image = tk_img
        print("[+] Viewing",plane_names[index])
        image_name_label.config(text=plane_names[index])

    def show_next_image():
        nonlocal index
        
        index+=1
        if index == len(image_names):
            index = 0
        img = im.open(image_names[index])
        img = img.resize((display_width, display_height), im.NEAREST)
        tk_img = ImageTk.PhotoImage(img)
        panel.configure(image=tk_img)
        panel.image = tk_img
        print("[+] Viewing",plane_names[index])
        image_name_label.config(text=plane_names[index])

    prev_btn = Button(root,text="Prev",command=show_prev_image).place(x=100, y=10)
    next_btn = Button(root,text="Next",command=show_next_image).place(x=140, y=10)
    
    save_btn = Button(root, text = 'Save Plane', command= lambda: saveimage(image_names[index])).place(x=240, y=10)

def openfilename(): 
    filename = filedialog.askopenfilename(title = "Open") 
    return filename

def saveimage(img_location):
    files = [("PNG File", '*.png')]
    filename = filedialog.asksaveasfile(filetypes = files, defaultextension = files)
    if filename=="":
        print("[-] No location selected for saving")
        return None
    print("[+] Saving current plane at", filename.name)
    img = im.open(img_location)
    img.save(filename.name)

if __name__ == "__main__":
    #location = r"test/bitplane.png"  
    #analyse(location)
    print("[+] Creating temporary folder named 'bitplane-temp'")

    if not os.path.exists('bitplane-temp'):
        os.makedirs('bitplane-temp')

    root = Tk()
    root.title("RGB Bit Plane Slicing")
    root.geometry("300x150") 
    root.resizable(width = True, height = True)

    btn = Button(root, text ='Load Image', command = analyse).place(x=10, y=10)

    panel = Label(root, image = None)
    panel.place(x=10, y=40)

    image_name_label = Label(root, text="")
    image_name_label.place(x=180, y=10)
    
    root.mainloop()
    
    print("[+] Deleting temporary folder named 'bitplane-temp' and its content")

    image_names=glob.glob('bitplane-temp\\*.png')
    for i in image_names:
        if os.path.exists(i):
            os.remove(i)

    if os.path.exists('bitplane-temp'):
        os.rmdir('bitplane-temp')
    
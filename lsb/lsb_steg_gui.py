import numpy as np
from PIL import Image as im
from itertools import permutations

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext

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

def extract(img_arr, channel_order, bit_start, bit_end, msg_len):
    hidden_msg = ""
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

def check_readability(b_string, min_readable_characters=0):
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

def analyse(image_location, bit_start, bit_end):

    if image_location=="":
        print("[-] Image not selected")
        messagebox.showerror("Error", "Image not selected")
        return None

    if bit_start>=bit_end:
        print("[-] Invalid Bit Range Selected")
        messagebox.showerror("Error", "Invalid Bit Range Selected")
        return None

    img = im.open(image_location)
    img_arr = np.array(img)

    search = search_box.get("1.0", "end-1c")
    byte_search = bytearray()
    byte_search.extend(map(ord, search))
    search = byte_search

    min_readable_characters = readable_chars_box.get("1.0", "end-1c")
    if min_readable_characters == "":
        min_readable_characters = 0
    elif not min_readable_characters.isnumeric():
        print("[-] Enter an integer in Continuous Readable Characters")
        messagebox.showerror("Error", "Enter an integer in Continuous Readable Characters") 
        return None
    else:
        min_readable_characters = int(min_readable_characters)

    msg_len = msg_len_box.get("1.0", "end-1c")
    if msg_len == "":
        msg_len = 500
    elif not msg_len.isnumeric():
        print("[-] Enter an integer in Number of bits to extract")
        messagebox.showerror("Error", "Enter an integer in Number of bits to extract")
        return None
    else:
        msg_len = int(msg_len)

    print(search, min_readable_characters)
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
        print("[-] Invalid Image Mode")
        messagebox.showerror("Error", "The image format is not supported")
        return None

    if bit_end-bit_start==1:
        print("[=] Checking bit number", bit_start+1, "\n")
    else:
        print("[=] Checking from bit", bit_start+1, "to", bit_end, "\n")

    if search!=b"":
        search_string = "".join(chr(i) for i in search)
        print("[=] Searching for keyword", search_string)

    results_window = Toplevel(root)
    listbox = Listbox(results_window, width=80, height=10)
    scrollbary = Scrollbar(results_window)
    scrollbarx = Scrollbar(results_window, orient="horizontal")
    listbox['font'] = ('consolas', '12')
    scrollbarx.pack(side = BOTTOM, fill = X)
    listbox.pack(side = LEFT, fill = BOTH)
    scrollbary.pack(side = RIGHT, fill = BOTH)

    listbox.config(yscrollcommand = scrollbary.set)
    scrollbary.config(command = listbox.yview)
    
    listbox.config(xscrollcommand = scrollbarx.set)
    scrollbarx.config(command = listbox.xview)

    for test in channel_orders:
        channel_order = [img.mode.index(channel) for channel in test]
        bin_msg = extract(img_arr, channel_order, bit_start, bit_end, msg_len)
        ascii_msg = bin_to_ascii(bin_msg)
        if (search in ascii_msg) and check_readability(ascii_msg, min_readable_characters):
            listbox.insert(END, test + " - " + "".join(map(chr, ascii_msg)))
            print("[+]", test, "-", "".join(map(chr, ascii_msg)))
            #print("[+]", test, "-", ascii_msg)
#img = im.open("test/test0.png", "r")
#img_arr = np.array(img)
#bin_msg = extract(img_arr, [0,1,2], 7, 8, 500)
#print(bin_to_ascii(bin_msg))

#analyse(img, 6, 8, 500, b"", 5)

def openimage():
    global image_location
    filename = filedialog.askopenfilename(title = "Open") 
    image_location = filename
    image_location_label.configure(text=image_location)
    
def savetxt(image_location, bit_start, bit_end, channels):
    
    if image_location=="":
        print("[-] Image not selected")
        messagebox.showerror("Error", "Image not selected") 
        return None

    if bit_start>=bit_end:
        print("[-] Invalid Bit Range Selected")
        messagebox.showerror("Error", "Invalid Bit Range Selected")
        return None

    files = [("Text File", '*.txt')]
    filename = filedialog.asksaveasfile(filetypes = files, defaultextension = files)
    if filename==None:
        messagebox.showerror("Error", "No location selected for saving")
        print("[-] No location selected for saving")
        return None
        
    img = im.open(image_location)
    img_arr = np.array(img)

    msg_len = msg_len_box.get("1.0", "end-1c")
    if msg_len == "":
        msg_len = 500
    elif not msg_len.isnumeric():
        print("[-] Enter an integer in Number of bits to extract")
        messagebox.showerror("Error", "Enter an integer in Number of bits to extract")
        return None
    else:
        msg_len = int(msg_len)

    for channel in channels:
        if channel not in img.mode:
            return None

    channel_order = []
    for channel in channels:
        channel_order.append(img.mode.index(channel))

    bin_msg = extract(img_arr, channel_order, bit_start, bit_end, msg_len)
    #ascii_msg = "".join(map(chr, bin_to_ascii(bin_msg)))
    ascii_msg = bin_to_ascii(bin_msg)

    with open(filename.name, "wb") as f:
        f.write(ascii_msg)
        print("[+] Data saved successfully")
        messagebox.showinfo("Successful", "Data Saved Successfully")


def unhide(image_location, bit_start, bit_end, channels):
    
    if image_location=="":
        print("[-] Image not selected")
        messagebox.showerror("Error", "Image not selected")
        return None

    if bit_start>=bit_end:
        print("[-] Invalid Bit Range Selected")
        messagebox.showerror("Error", "Invalid Bit Range Selected")
        return None
        
    img = im.open(image_location)
    img_arr = np.array(img)

    msg_len = msg_len_box.get("1.0", "end-1c")
    if msg_len == "":
        msg_len = 500
    elif not msg_len.isnumeric():
        print("[-] Enter an integer in Number of bits to extract")
        messagebox.showerror("Error", "Enter an integer in Number of bits to extract")
        return None
    else:
        msg_len = int(msg_len)

    for channel in channels:
        if channel not in img.mode:
            return None

    channel_order = []
    for channel in channels:
        channel_order.append(img.mode.index(channel))

    bin_msg = extract(img_arr, channel_order, bit_start, bit_end, msg_len)
    ascii_msg = "".join(map(chr, bin_to_ascii(bin_msg)))

    msg_window = Toplevel(root)
    msg_window.geometry("420x300")
    """ msg_label = Text(msg_window, width=45, wrap=CHAR)
    msg_label.insert(END, ascii_msg)
    msg_label.config(state=DISABLED)
    msg_label.place(x=10, y=10)

    scrollbar = Scrollbar(msg_window, command=msg_label.yview)
    scrollbar.pack(side = RIGHT, fill = BOTH)

    msg_label.config(yscrollcommand=scrollbar.set) """
    txt = scrolledtext.ScrolledText(msg_window, undo=True)
    txt['font'] = ('consolas', '12')
    txt.pack(expand=True, fill='both')
    txt.insert(END,ascii_msg)
    txt.config(state=DISABLED)
    print("[+]", ascii_msg)
    msg_window.mainloop()


if __name__ == "__main__":

    if os.name == "nt":
        space_adjust = 1
    else:
        space_adjust = 0

    image_location = ""

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
    root.title("LSB Steg")
    root.geometry("300x350") 
    root.resizable(width = True, height = True)

    img_btn = Button(root, text="Load Image", command=openimage).place(x=10, y=10)
    image_location_label = Label(root, text="")
    image_location_label.place(x=120, y=15)

    channels = StringVar(root)
    channels.set(channel_names[0])
    channels_dropdown = OptionMenu(root, channels, *channel_names).place(x=120 - space_adjust*20, y=50)

    bit_start = IntVar(root)
    bit_end = IntVar(root)
    
    bit_start.set(8)
    bit_end.set(8)

    bit_start_dropdown = OptionMenu(root, bit_start, *bits).place(x=75 - space_adjust*5, y=90)
    bit_end_dropdown = OptionMenu(root, bit_end, *bits).place(x=75 - space_adjust*5, y=130)

    channels_label = Label(root, text="Channel Order: ").place(x=10, y=55)
    bit_start_label = Label(root, text="Bit Start: ").place(x=10, y=95)
    bit_end_label = Label(root, text="Bit End: ").place(x=10, y=135)

    msg_len_label = Label(root, text="Number of bits to extract: ").place(x=10, y=175)
    msg_len_box = Text(root, height=1, width=12)
    msg_len_box.place(x=190 - space_adjust*30, y=175)

    search_label = Label(root, text="Search keyword: ").place(x=10, y=215)
    search_box = Text(root, height=1, width=19)
    search_box.place(x=130 - space_adjust*20, y=215)

    readable_chars_label = Label(root, text="Continuous readable chars: ").place(x=10, y=255)
    readable_chars_box = Text(root, height=1, width=9)
    readable_chars_box.place(x=200 - space_adjust*10, y=255)

    analyse_btn = Button(root, text="Analyse", command=lambda: analyse(image_location, bit_start.get()-1, bit_end.get())).place(x=80 - space_adjust*20, y=300)
    
    save_btn = Button(root, text="Save", command=lambda: savetxt(image_location, bit_start.get()-1, bit_end.get(), channels.get())).place(x=165 - space_adjust*40, y=300)
    unhide_btn = Button(root, text="Show", command=lambda: unhide(image_location, bit_start.get()-1, bit_end.get(), channels.get())).place(x=10, y=300)
    root.mainloop()
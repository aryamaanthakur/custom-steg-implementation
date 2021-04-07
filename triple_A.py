from hashlib import sha256
#from Crypto.Protocol.KDF import PBKDF2
from Crypto.Cipher import AES
from PIL import Image
import numpy as np
import random

password = "1337h4x0r"
data = "this is plain text"

def Encrypt(data, key):
    cipher_encrypt = AES.new(key, AES.MODE_CFB, iv=key[:16])
    ciphered_bytes = cipher_encrypt.encrypt(data)

    return ciphered_bytes

def Decrypt(ciphered_data, key):

    cipher_decrypt = AES.new(key, AES.MODE_CFB, iv=key[:16])
    deciphered_bytes = cipher_decrypt.decrypt(ciphered_data)

    return deciphered_bytes

#key = PBKDF2(password, "", dkLen=32)


""" ciphered_data = Encrypt(data.encode(), key)
print(ciphered_data)
deciphered_data = Decrypt(ciphered_data[:10], key)
print(deciphered_data) """

def hide(image_location, data, password):

    img = Image.open(image_location)
    img_arr = np.array(img.getdata())
    img_len, n = img_arr.shape
    width, height = img.size

    key = sha256(password.encode()).digest()
    ciphered_data = Encrypt(data.encode("utf-8"), key)
    print("c",ciphered_data)
    bin_msg = "".join(f'{i:08b}' for i in ciphered_data)
    print("c", bin_msg)
    msg_len = len(bin_msg)
    msg_index = 0

    random.seed(password.encode("utf-8"))
    for img_index in range(img_len):

        pixel = img_arr[img_index]

        channel_prng = random.randint(0,6)
        #channel_names = ["R", "G", "B", "RG", "RB", "GB", "RGB"]
        channel_names = [[0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2]]
        channels = channel_names[channel_prng]
    
        bits_prng = random.randint(1,3)
        bits_len = bits_prng

        
        current_msg_len = len(channels)*bits_len

        if msg_index+current_msg_len > msg_len:
            current_msg = bin_msg[msg_index:]+"0"*(current_msg_len - msg_len + msg_index)
            #print(current_msg)
        else:
            current_msg = bin_msg[msg_index:msg_index+current_msg_len]
        #print(img_index, channels, bits_len, msg_index, current_msg)
        msg_index+=current_msg_len

        for channel in channels:
            curr_value = f'{pixel[channel]:08b}'
            new_value = curr_value[0:(8-bits_len)]+current_msg[0:bits_len]
            img_arr[img_index][channel] = new_value

            current_msg = current_msg[bits_len:]

        if msg_index>=msg_len:
            break
        
    img_arr=img_arr.reshape(height, width, n)
    new_img = Image.fromarray(img_arr.astype('uint8'), img.mode)
    new_img.save("test\\flag0.png")
    print("Image Encoded Successfully")

image_location = "test\\flag.png"
hide(image_location, data, password)

def unhide(image_location, password, cycles):

    img = Image.open(image_location)
    img_arr = np.array(img.getdata())

    key = sha256(password.encode()).digest()
    
    msg = ""

    random.seed(password.encode("utf-8"))
    for img_index in range(cycles):

        pixel = img_arr[img_index]

        channel_prng = random.randint(0,6)
        #channel_names = ["R", "G", "B", "RG", "RB", "GB", "RGB"]
        channel_names = [[0], [1], [2], [0, 1], [0, 2], [1, 2], [0, 1, 2]]
        channels = channel_names[channel_prng]
    
        bits_prng = random.randint(1,3)
        bits_len = bits_prng

        
        current_msg = ""

        for channel in channels:
            curr_value = f'{pixel[channel]:08b}'
            current_msg += curr_value[(8-bits_len):]
        
        msg+=current_msg

    """ if len(msg)%8 != 0:
        msg+="0"*(8 - len(msg)%8) """
    ciphered_data = bytearray()
    for i in range(0, len(msg), 8):
        x = int(msg[i:i+8], 2)
        ciphered_data.append(x)
    print("d", msg)
    print("d", ciphered_data)
    deciphered_data = Decrypt(ciphered_data, key)
    print(deciphered_data)

unhide("test\\flag0.png", password, 45)
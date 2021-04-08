# Custom Steganography Implementation

## Description

This project consists of 3 subparts :-

1. Least Significant Bit Steganography
2. Bit Plane Slicing Steganography
3. Triple-A Steganography Technique (based on a research paper)

## Installation

`$ git clone https://github.com/aryamaanthakur/custom-steg-implementation.git`

`$ cd custom-steg-implementation`

`$ pip3 install -r requirements.txt`

## Usage

### Least Significant Bit Steganography

`$ python3 csi.py lsbh`

Click on the **Load Image** button and select a PNG/JPG image. Now select a TXT file which contains the data to be hidden by clicking on the **Load Text** button.

Select the **Channel Order** in which you want to hide the text. Make sure to select Alpha Plane only when your image has the 4th channel or you will receive a warning.

**Bit Start** and **Bit End** are range of positions (in 8 bit binary representation of pixel values) which will be used for hiding. 1 stands for the left most digit and 8 for the least significant digit.

*For Example: If Bit Start = 7 and Bit End = 8 then 2 least significant bits will be used and if Bit Start = 1 and Bit End = 3 then 3 most significant bits will be used for hiding data*

Clicking on the **Hide** button will ask for the location and name of new image.

`$ python3 csi.py lsbu`

#### Analyse
This will display the results obtained from all the channels and specified bit range.
#### Show
This will check and display only the channel order and bit range specified using the dropdowns.
#### Save
This will save the data obtained from a particular channel order and bit range as a text file.

**Number of bits to extract:** Default is 500 bits

**Search Keyword:** You can search for specific keywords while using the analyse feature.

**Continuous Readable Characters:** You can filter the results of analysis so that only those channels are displayed where continuous readable characters are present. Default is 0.

### RGB Bit Plane Slicing

`python3 csi.py bps`

**Load** an image and wait (it takes time to process large images but it will work for sure).
Once all the bitplanes are generated you can navigate between them using the **Next** and **Prev** buttons.

You can also save a particular plane with the **Save Plane** button.

**Note:** Large files of 10-12 MB can take upto 2 minutes or sometimes even more depending on available resources.


*Tip: The planes are stored in a temporary folder created in the same directory, you can view the images directly from that folder too in full resolution.*

`python3 csi.py bph`

Select the respective images by clicking on the buttons and browsing to a location. Make sure the image to be hidden is smaller than host image in dimensions or you'll receive a warning.

The secret image is converted to a Black & White Image before encoding and then it is hidden based on the plane selected from dropdown.

0 stands for Most Significant Bit and 7 stands for Least Significant Bit.

### Triple - A Steganography Technique

This is an implementation of following research paper, the abstract is also mentioned below.

[Gutub, Adnan & Al-Qahtani, Ayed & Tabakh, Abdulaziz. (2009). Triple-A: Secure RGB Image Steganography Based on Randomization. 400 - 403. 10.1109/AICCSA.2009.5069356.](https://www.researchgate.net/publication/224503189_Triple-A_Secure_RGB_Image_Steganography_Based_on_Randomization)

`$ python3 csi.py triplea`

Click on the **Load Image** button and select an image. Also select a text file using the **Load Text** button only if you want to use the hide option.

**Number of Cycles to perform:** Used only when extracting data. Cycle refers to the process of generating random numbers using the seed and extracting the hidden bits. Default is 50.

**Password:** This password will be used to generate the key for AES and will also be used in seeding. *You forget this and there's no way to reverse things*

**Abstract**

A new image-based steganography technique-called triple-A algorithm is proposed in this paper. It uses the same principle of LSB, where the secret is hidden in the least significant bits of the pixels, with more randomization in selection of the number of bits used and the color channels that are used. This randomization is expected to increase the security of the system and also increase the capacity. This technique can be applied to RGB images where each pixel is represented by three bytes to indicate the intensity of red, green, and blue in that pixel.

## Post WoC Task
I will rename the files so they are easier to use and remove the non-GUI implementations or convert them to working CLI programs using `argparse`.

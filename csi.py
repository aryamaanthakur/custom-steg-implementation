import argparse
import os
#if __name__ == "__main__":
    
help_text = """      ___           ___                 
     /  /\         /  /\        ___     
    /  /:/        /  /:/_      /  /\    
   /  /:/        /  /:/ /\    /  /:/    
  /  /:/  ___   /  /:/ /::\  /__/::\    
 /__/:/  /  /\ /__/:/ /:/\:\ \__\/\:\__ 
 \  \:\ /  /:/ \  \:\/:/~/:/    \  \:\/\\
  \  \:\  /:/   \  \::/ /:/      \__\::/
   \  \:\/:/     \__\/ /:/       /__/:/ 
    \  \::/        /__/:/        \__\/  
     \__\/         \__\/                
                                              

A custom steganography implementation for RGB bit plane, Least Significant Bit (LSB)
and Triple-A steganography.

Use the following arguments to open corresponding applications:

    bph : Bit Plane Hiding
    bps : Bit Plane Slicing
    lsbh : LSB Hiding
    lsbu : LSB Unhiding
    triplea: Triple-A Steganography

Visit https://github.com/aryamaanthakur/custom-steg-implementation for more help."""

parser = argparse.ArgumentParser(description = help_text, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('command', choices = ['bph', 'bps', 'lsbh', 'lsbu', 'triplea'])

args = parser.parse_args()

if args.command=="bps":
    path = os.path.join(os.getcwd(), "bitplane/bit_plane_slicing_gui.py")

elif args.command=="bph":
    path = os.path.join(os.getcwd(), "bitplane/bit_plane_hiding_gui.py")

elif args.command=="lsbh":
    path = os.path.join(os.getcwd(), "lsb/lsb_steg_hiding_gui.py")

elif args.command=="lsbu":
    path = os.path.join(os.getcwd(), "lsb/lsb_steg_gui.py")

elif args.command=="triplea":
    path = os.path.join(os.getcwd(), "triplea/triple_A_gui.py")

else:
    path = ""

if path != "":
    with open(path, "rb") as source_file:
        code = compile(source_file.read(), path, "exec")
    exec(code)
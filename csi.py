import argparse
import os
#if __name__ == "__main__":
    
help_text = "This is help"
parser = argparse.ArgumentParser()
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
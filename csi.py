import argparse
import os
#if __name__ == "__main__":
    
help_text = "This is help"
parser = argparse.ArgumentParser()
parser.add_argument('command', choices = ['bph', 'bps', 'lsbh', 'lsbu', 'triplea'])

args = parser.parse_args()

if args.command=="bps":
    with open("bitplane\\bit_plane_slicing_gui.py", "rb") as source_file:
        code = compile(source_file.read(), "bitplane\\bit_plane_slicing_gui.py", "exec")
    #os.system("python3 bit_plane_slicing_gui.py")
elif args.command=="bph":
    with open("bitplane\\bit_plane_hiding_gui.py", "rb") as source_file:
        code = compile(source_file.read(), "bitplane\\bit_plane_hiding_gui.py", "exec")

elif args.command=="lsbh":
    with open("lsb\\lsb_steg_hiding_gui.py", "rb") as source_file:
        code = compile(source_file.read(), "lsb\\lsb_steg_hiding_gui.py", "exec")

elif args.command=="lsbu":
    with open("lsb\\lsb_steg_gui.py", "rb") as source_file:
        code = compile(source_file.read(), "lsb\\lsb_steg_gui.py", "exec")

elif args.command=="triplea":
    with open("tripleA\\triple_A_gui.py", "rb") as source_file:
        code = compile(source_file.read(), "triplea\\triple_A_gui.py.py", "exec")
    #os.system("python3 triple_A_gui.py")
else:
    code = ""

if code != "":
    exec(code)
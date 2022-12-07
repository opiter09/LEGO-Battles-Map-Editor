import PySimpleGUI as psg
import random
import os
import subprocess

if (os.path.exists("LEGO BATTLES") == False):
    filename = psg.popup_get_file("Enter your ROM file:", file_types = [("NDS Files", "*.nds")])
    subprocess.run([ "java", "-jar", "jNDSTool-1.0.1.jar", "-x", filename, "-d", "LEGO BATTLES" ])

if (os.path.exists("KingTileset.png") == False):
    psg.popup("You will now need to convert each of the tilesets to a PNG. NitroPaint will automatically open three times in a row. Each time \
you must press File -> Export, then save the PNG as XXXTileset.png in the same folder as this exe, where XXX = King, then Mars, then Pirate. \
Then just X out of NitroPaint, and it will immediately open again for the next one.")

    subprocess.run([ "NitroPaint.exe", "LEGO BATTLES/data/KingTileset.NCGR", "LEGO BATTLES/data/KingTileset.NCLR" ])
    subprocess.run([ "NitroPaint.exe", "LEGO BATTLES/data/MarsTileset.NCGR", "LEGO BATTLES/data/MarsTileset.NCLR" ])
    subprocess.run([ "NitroPaint.exe", "LEGO BATTLES/data/PirateTileset.NCGR", "LEGO BATTLES/data/PirateTileset.NCLR" ])
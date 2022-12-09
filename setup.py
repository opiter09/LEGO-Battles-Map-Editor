import PySimpleGUI as psg
import random
import os
import subprocess
import shutil
from PIL import Image
import numpy as np

def runSetup():
    if (os.path.exists("LEGO BATTLES") == False):
        filename = psg.popup_get_file("Enter your ROM file:", file_types = [("NDS Files", "*.nds")])
        subprocess.run([ "java", "-jar", "jNDSTool-1.0.1.jar", "-x", filename, "-d", "LEGO BATTLES" ])

    if (os.path.exists("Tilesets") == False):
        psg.popup("You will now need to convert each of the tilesets to a PNG. NitroPaint will automatically open three times in a row. Each time \
you must press File -> Export, then save the PNG as XXXTileset.png in the same folder as this exe, where XXX = King, then Mars, then Pirate. \
Then just X out of NitroPaint, and it will immediately open again for the next one.")

        subprocess.run([ "NitroPaint.exe", "LEGO BATTLES/data/KingTileset.NCLR", "LEGO BATTLES/data/KingTileset.NCGR" ])
        subprocess.run([ "NitroPaint.exe", "LEGO BATTLES/data/MarsTileset.NCLR", "LEGO BATTLES/data/MarsTileset.NCGR" ])
        subprocess.run([ "NitroPaint.exe", "LEGO BATTLES/data/PirateTileset.NCLR", "LEGO BATTLES/data/PirateTileset.NCGR" ])

        os.makedirs("Tilesets")
        os.rename("KingTileset.png", "Tilesets/KingTileset.png")
        os.rename("MarsTileset.png", "Tilesets/MarsTileset.png")
        os.rename("PirateTileset.png", "Tilesets/PirateTileset.png")
        for name in ["KingTileset", "MarsTileset", "PirateTileset"]:
            os.makedirs("./Tilesets/" + name)
            im = Image.open("./Tilesets/" + name + ".png")
            imgwidth, imgheight = im.size
            count = -1
            for i in range(0, imgheight, 8):
                for j in range(0, imgwidth, 8):
                    count = count + 1
                    piece = im.crop((j, i, j + 8, i + 8))
                    piece.save("./Tilesets/" + name + "/" + str(count).zfill(4) + ".png")             
    
    if (os.path.exists("Current Blocks") == False):
        os.makedirs("Current Blocks")
    else:
        for root, dirs, files in os.walk("./Current Blocks"):
            for file in files:
                os.remove(os.path.join(root, file))
        

    if (os.path.exists("Backup Maps") == False):
        shutil.copytree("LEGO BATTLES/data/Maps", "Backup Maps")

    if (os.path.exists("Uncompressed Maps") == False):
        os.makedirs("Uncompressed Maps")
        for root, dirs, files in os.walk("LEGO BATTLES/data/Maps"):
            for file in files:
                opening = open(os.path.join(root, file), "rb")
                reading = opening.read()
                opening.close()
                
                newFile = open("./Uncompressed Maps/" + file, "wb")
                newFile.close()
                newFile = open("./Uncompressed Maps/" + file, "ab")
                
                segNumber = int.from_bytes(reading[8:12], "little")
                offset = 16 + 4 * segNumber
                for i in range(segNumber):
                    size = int.from_bytes(reading[(16 + (i * 4)):(20 + (i * 4))], "little")
                    tempFile = open("temp_" + str(i).zfill(3) + ".bin", "wb")
                    tempFile.write(reading[offset:(offset + size)])
                    tempFile.close()
                    subprocess.run([ "lzx.exe", "-d", "temp_" + str(i).zfill(3) + ".bin" ])
                    tempFile = open("temp_" + str(i).zfill(3) + ".bin", "rb")
                    newFile.write(tempFile.read())
                    tempFile.close()
                    os.remove("temp_" + str(i).zfill(3) + ".bin")
                    offset = offset + size
                newFile.close()
                
    if (os.path.exists("Backup BP") == False):
        shutil.copytree("LEGO BATTLES/data/BP", "Backup BP")

    if (os.path.exists("Uncompressed BP") == False):
        os.makedirs("Uncompressed BP")
        for root, dirs, files in os.walk("LEGO BATTLES/data/BP"):
            for file in files:
                opening = open(os.path.join(root, file), "rb")
                reading = opening.read()
                opening.close()
                
                newFile = open("./Uncompressed BP/" + file, "wb")
                newFile.close()
                newFile = open("./Uncompressed BP/" + file, "ab")
                
                segNumber = int.from_bytes(reading[8:12], "little")
                offset = 16 + 4 * segNumber
                for i in range(segNumber):
                    size = int.from_bytes(reading[(16 + (i * 4)):(20 + (i * 4))], "little")
                    tempFile = open("temp_" + str(i).zfill(3) + ".bin", "wb")
                    tempFile.write(reading[offset:(offset + size)])
                    tempFile.close()
                    subprocess.run([ "lzx.exe", "-d", "temp_" + str(i).zfill(3) + ".bin" ])
                    tempFile = open("temp_" + str(i).zfill(3) + ".bin", "rb")
                    newFile.write(tempFile.read())
                    tempFile.close()
                    os.remove("temp_" + str(i).zfill(3) + ".bin")
                    offset = offset + size
                newFile.close()
                    
                
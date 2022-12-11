import PySimpleGUI as psg
import random
import os
import subprocess
import shutil
from PIL import Image
import numpy as np

def runSetup():
    if (os.path.exists("LEGO BATTLES") == False):
        os.makedirs("LEGO BATTLES")
        filename = psg.popup_get_file("Enter your ROM file:", file_types = [("NDS Files", "*.nds")])
        subprocess.run([ "./ndstool.exe", "-x", filename, "-d", "LEGO BATTLES/data",  "-y", "LEGO BATTLES/overlay", "-9", "LEGO BATTLES/arm9.bin",
            "-7", "LEGO BATTLES/arm7.bin", "-y9", "LEGO BATTLES/arm9ovltable.bin", "-y7", "LEGO BATTLES/arm7ovltable.bin",
            "-t", "LEGO BATTLES/banner.bin", "-h", "LEGO BATTLES/header.bin", "-o", "LEGO BATTLES/logo.bin" ])

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
    
    if (os.path.exists("All Blocks") == False):
        os.makedirs("All Blocks")
        for root, dirs, files in os.walk("Uncompressed BP"):
            for file in [ x for x in files if (x.endswith(".tbp") == True) ]:
                opening = open(os.path.join(root, file), "rb")
                reading = opening.read()
                opening.close()
                if (file[0:-4].endswith("Tiles") == True):
                    folder = "All Blocks/" + file[0:-4] + "et"
                    os.makedirs(folder)
                    count = -1
                    tileset = file[0:-4] + "et"
                else:
                    folder = "All Blocks/" + file[0:-4].split("_", 1)[1]
                    os.makedirs(folder)
                    count = 439
                    try:
                        mapF = open("Uncompressed Maps/" + file[0:-4].split("_", 1)[1] + ".map", "rb")
                        tileset = mapF.read()[11:24].decode("UTF-8").replace("\0", "")
                        mapF.close()
                    except FileNotFoundError as error:
                        continue
                    
                for i in range(int.from_bytes(reading[0:2], "little")):
                    count = count + 1
                    if (count == 440) and (file[0:-4].endswith("Tiles") == True):
                        break
                    ID = []
                    tiles = []
                    new = Image.new("RGB", (24, 16))
                    for j in range(2, 14, 2):
                        ID.append(int.from_bytes(reading[(j + (i * 12)):(j + 2 + (i * 12))], "little"))
                    if (max(ID) >= 1024):
                        continue
                    for j in range(6):                           
                        tiles.append(Image.open("Tilesets/" + tileset + "/" + str(ID[j]).zfill(4) + ".png"))
                    new.paste(tiles[0], (0, 0))
                    new.paste(tiles[1], (8, 0))
                    new.paste(tiles[2], (16, 0))
                    new.paste(tiles[3], (0, 8))
                    new.paste(tiles[4], (8, 8))
                    new.paste(tiles[5], (16, 8))
                    new.save(folder + "/" + str(count).zfill(4) + "_" + str(ID[0]) + "-" + str(ID[1]) + "-" + str(ID[2]) + "-"
                        + str(ID[3]) + "-" + str(ID[4]) + "-" + str(ID[5]) + ".png")
                    
                
                    
                
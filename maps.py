import PySimpleGUI as psg
import random
import os
import subprocess
import shutil
from PIL import Image
from setup import runSetup

runSetup()

filename = psg.popup_get_file("Enter your MAP file:", file_types = [("MAP Files", "*.map")])
if (os.path.exists("All Blocks/" + filename.split("/")[-1].split(".")[0]) == False):
    print("This map file has no block set!")
    exit()
opening = open(filename, "rb")
reading = opening.read()
opening.close()

length = reading[7]
width = reading[8]
tileset = reading[11:24].decode("UTF-8").replace("\0", "")

offset = 0x2B + 3 * length * width + 2 + int.from_bytes(reading[(0x2B + 3 * length * width):(0x2B + 3 * length * width + 2)], "little")
tileList = []
bigImage = Image.new("RGB", (length * 24, width * 16))
x = -1
y = 0
for i in range(offset, offset + 2 * length * width, 2):
    x = x + 1
    if (x >= length):
        x = 0
        y = y + 1
    tile = int.from_bytes(reading[i:(i + 2)], "little")
    tileList.append(tile)
    if (tile <= 439):
        for root, dirs, files in os.walk("All Blocks/" + tileset):
            for file in files:
                if (int(file.split("_")[0]) == tile):
                    bigImage.paste(Image.open(os.path.join(root, file)), (x * 24, y * 16))
                    break
    else:
        for root, dirs, files in os.walk("All Blocks/" + filename.split("/")[-1].split(".")[0]):
            for file in files:
                if (int(file.split("_")[0]) == tile):
                    bigImage.paste(Image.open(os.path.join(root, file)), (x * 24, y * 16))
                    break
bigImage.save("currentMap.png")
window = psg.Window("", [ [psg.Image("currentMap.png")] ], grab_anywhere = True, resizable = True)
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if (event == psg.WINDOW_CLOSED) or (event == "Quit"):
        break
# Finish up by removing from the screen
window.close()
                    
                    

import PySimpleGUI as psg
import random
import os
import subprocess
import shutil
from PIL import Image
import setup
import build

setup.runSetup()

filename = psg.popup_get_file("Enter your Map file:", file_types = [("MAP Files", "*.map")])
if (os.path.exists("All Blocks/" + filename.split("/")[-1].split(".")[0]) == False):
    print("This map file has no block set!")
    exit()
opening = open(filename, "rb")
reading = opening.read()
opening.close()

length = reading[7]
width = reading[8]
tileset = reading[11:24].decode("UTF-8").replace("\0", "")

layer1 = []
for i in range(0x2B, 0x2B + length * width):
    layer1.append(reading[i])
layer2 = []
for i in range(0x2B + length * width, 0x2B + 2 * length * width):
    layer2.append(reading[i])
layer3 = []
for i in range(0x2B + 2 * length * width, 0x2B + 3 * length * width):
    layer3.append(reading[i])

trees = []
stripCount = int.from_bytes(reading[(0x2B + 3 * length * width):(0x2B + 3 * length * width + 2)], "little")
pos = 0
for i in range(stripCount):
    trees = trees + [pos] * reading[0x2B + 3 * length * width + 2 + i]
    pos = int(not pos)

offset = 0x2B + 3 * length * width + 2 + stripCount
tileList = []
imageList = []
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
                    imageList.append(os.path.join(root, file))
                    bigImage.paste(Image.open(os.path.join(root, file)), (x * 24, y * 16))
                    break
    else:
        for root, dirs, files in os.walk("All Blocks/" + filename.split("/")[-1].split(".")[0]):
            for file in files:
                if (int(file.split("_")[0]) == tile):
                    imageList.append(os.path.join(root, file))
                    bigImage.paste(Image.open(os.path.join(root, file)), (x * 24, y * 16))
                    break
bigImage.save("currentMap.png")
unknown = reading[(offset + 2 * length * width):]

layout = [
    [ psg.Button("Build ROM"), psg.Button("Build DetailTiles"), psg.Button("Build Map") ],
    [
        psg.Button("Top Half"),
        psg.Button("Bottom Half"),
        psg.DropDown(["KingTileset", "MarsTileset", "PirateTileset"], default_value = tileset, enable_events = True, key = "drop")
    ]
]
window = psg.Window("", layout, grab_anywhere = True, resizable = True)
while True:
    event, values = window.read()
    # See if user wants to quit or window was closed
    if (event == psg.WINDOW_CLOSED) or (event == "Quit"):
        break
    elif (event == "Build ROM"):
        build.buildROM()
        psg.popup("ROM successfully built!")
    elif (event == "Build DetailTiles"):
        build.buildDetailTiles(filename.split("/")[-1].split(".")[0])
        psg.popup("Block file successfully built!")
    elif (event == "Build Map"):
        bigDataList = [ layer1, layer2, layer3, trees, tileList, unknown ]
        build.buildMap(filename.split("/")[-1].split(".")[0], length, width, tileset, bigDataList)
        psg.popup("Map file successfully built!")
    elif (event == "drop"):
        tileset = values["drop"]
# Finish up by removing from the screen
window.close()
                    
                    

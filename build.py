import os
import subprocess
import shutil

def buildROM():
    shutil.rmtree("LEGO BATTLES/data/BP")
    shutil.copytree("Uncompressed BP", "LEGO BATTLES/data/BP")
    for root, dirs, files in os.walk("LEGO BATTLES/Data/BP"):
        for file in files:
            subprocess.run([ "lzx.exe", "-evb", os.path.join(root, file) ])
            opening = open(os.path.join(root, file), "rb")
            reading = opening.read()
            opening.close()
            opening = open(os.path.join(root, file), "wb")
            opening.close()
            opening = open(os.path.join(root, file), "ab")
            opening.write(("PMOC").encode("UTF-8"))
            opening.write((os.stat("Uncompressed BP/" + file).st_size).to_bytes(4, "little"))
            opening.write((1).to_bytes(4, "little"))
            opening.write(len(reading).to_bytes(4, "little"))
            opening.write(len(reading).to_bytes(4, "little"))
            opening.write(reading)
            opening.close()
            
    shutil.rmtree("LEGO BATTLES/data/Maps")
    shutil.copytree("Uncompressed Maps", "LEGO BATTLES/data/Maps")
    for root, dirs, files in os.walk("LEGO BATTLES/Data/Maps"):
        for file in files:
            subprocess.run([ "lzx.exe", "-evb", os.path.join(root, file) ])
            opening = open(os.path.join(root, file), "rb")
            reading = opening.read()
            opening.close()
            opening = open(os.path.join(root, file), "wb")
            opening.close()
            opening = open(os.path.join(root, file), "ab")
            opening.write(("PMOC").encode("UTF-8"))
            opening.write((os.stat("Uncompressed Maps/" + file).st_size).to_bytes(4, "little"))
            opening.write((1).to_bytes(4, "little"))
            opening.write(len(reading).to_bytes(4, "little"))
            opening.write(len(reading).to_bytes(4, "little"))
            opening.write(reading)
            opening.close()

    subprocess.run([ "./ndstool.exe", "-c", "outputLB.nds", "-d", "LEGO BATTLES/data",  "-y", "LEGO BATTLES/overlay", "-9", "LEGO BATTLES/arm9.bin",
        "-7", "LEGO BATTLES/arm7.bin", "-y9", "LEGO BATTLES/arm9ovltable.bin", "-y7", "LEGO BATTLES/arm7ovltable.bin",
        "-t", "LEGO BATTLES/banner.bin", "-h", "LEGO BATTLES/header.bin", "-o", "LEGO BATTLES/logo.bin" ])

def buildDetailTiles(mapName):
    dFile = open("Uncompressed BP/DetailTiles_" + mapName + ".tbp", "wb")
    dFile.close()
    dFile = open("Uncompressed BP/DetailTiles_" + mapName + ".tbp", "ab")
    dFile.write(len(os.listdir("All Blocks/" + mapName)).to_bytes(2, "little"))
    for root, dirs, files in os.walk("All Blocks/" + mapName):
        for file in files:
            for num in file.split("_")[1].split(".")[0].split("-"):
                dFile.write(int(num).to_bytes(2, "little"))
    dFile.close()

def buildMap(mapName, length, width, tileset, bigDataList):
    mFile = open("Uncompressed Maps/" + mapName + ".map", "wb")
    mFile.close()
    mFile = open("Uncompressed Maps/" + mapName + ".map", "ab")
    mFile.write(("MAPTERR").encode("UTF-8"))
    mFile.write(length.to_bytes(1, "little"))
    mFile.write(width.to_bytes(1, "little"))
    mFile.write((0x0302).to_bytes(2, "big"))
    mFile.write(tileset.encode("UTF-8"))
    mFile.write(bytes(32 - len(tileset)))
    for i in range(3):
        for num in bigDataList[i]:
            mFile.write(num.to_bytes(1, "little"))
    convert = []
    pos = 0
    count = 0
    for num in bigDataList[3]:
        if (num == pos):
            count = count + 1
            if (count == 256):
                convert = convert + [255, 0]
                count = 1
        else:
            convert.append(count)
            count = 1
            pos = int(not pos)
    convert.append(count)
    mFile.write(len(convert).to_bytes(2, "little"))
    for num in convert:
        mFile.write(num.to_bytes(1, "little"))
    for num in bigDataList[4]:
        mFile.write(num.to_bytes(2, "little"))
    mFile.write(bigDataList[5])
    mFile.close()
    
        
    
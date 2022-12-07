import sys
import os
binn2 = open(sys.argv[1], "rb")
bytE = binn2.read()
binn2.close()

folder = sys.argv[1].split("\\")[-1].split(".")[0] + "_" + "langFiles/"

newFile = open("output_" + sys.argv[1].split("\\")[-1], "wb")
newFile.close()
newFile = open("output_" + sys.argv[1].split("\\")[-1], "ab")
newFile.write(bytE[0:16])

offset = int.from_bytes(bytE[12:16], "little")
for i in range(1, 3064):
    if (os.path.exists(folder + str(i).zfill(4) + ".bin") == True):
        size = os.stat(folder + str(i).zfill(4) + ".bin").st_size
        offset = offset + size
        newFile.write(offset.to_bytes(4, "little"))
    else:
        newFile.write(bytE[(12 + (i * 4)):(16 + (i * 4))])

for i in range(1, 3065):
    if (os.path.exists(folder + str(i).zfill(4) + ".bin") == True):
        file = open(folder + str(i).zfill(4) + ".bin", "rb")
        newFile.write(file.read())
        file.close()
newFile.close()
    

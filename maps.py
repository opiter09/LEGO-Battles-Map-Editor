import PySimpleGUI as psg
import random
import os
import subprocess
import shutil
from PIL import Image
from setup import runSetup

runSetup()

filename = psg.popup_get_file("Enter your MAP file:", file_types = [("MAP Files", "*.map")]) 
if (os.path.exists("All Blocks/" + filename.split("\\")[-1].split(".")[0]) == False):
    print("This map file has no block set!")
    exit()
opening = open(filename, "rb")
reading = opening.read()
opening.close()

length = reading[7]
width = reading[8]
tilset = reading[11:24].decode("UTF-8").replace("\0", "")

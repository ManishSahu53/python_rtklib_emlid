def check_dir(path):
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def booldialogbox(message):
    result = tkMessageBox.askquestion(
        "Provide you input", message, icon='warning')
    if result == 'yes':
        return 1
    else:
        return 0


import os
import sys
import subprocess
import pexif
import shutil
import shapefile
import numpy as np
import Tkinter
import Tkconstants
import tkFileDialog
import tkMessageBox
from Tkinter import *

import zipfile
from os.path import basename
import pandas as pd

root = Tk()

# Reading zip files
base_zip = tkFileDialog.askopenfilename(
    initialdir="/", title="Select Base ubx zip file", filetypes=(("zip files", "*.zip"), ("all files", "*.*")))
rover_zip = tkFileDialog.askopenfilenames(
    initialdir="/", title="Select Rover ubx files", filetypes=(("zip files", "*.zip"), ("all files", "*.*")))

# Asking for Position of Base
base_pos_prompt = booldialogbox("Do you want enter position of base?")

if base_pos_prompt == 1:  # Taking Base coordinates, then enter csv else continue
    base_pos = tkFileDialog.askopenfilename(
        initialdir="/", title="Select Position csv files", filetypes=(("csv file", "*.csv"), ("all files", "*.*")))

    # Reading csv as pandas dataframe and then numpy array
    # Lat, Long, Ele
    csv_pos = pd.read_csv(base_pos)
    csv_matrix = csv_pos.values
    lat = csv_matrix[0][0]
    long = csv_matrix[0][1]
    ele = csv_matrix[0][2]
    base_position = str(lat) + " " + str(long) + " " + str(ele)
    print(base_position)

# Is it static mode or kinematic mode
mode_prompt = booldialogbox(
    "Process with Static mode? Yes- Static mode, No- Kinematic mode")
if mode_prompt == 1:
    mode = str(3)  # Static
else:
    mode = str(2)  # Kinematic


# Setting executable path files
exe_path = 'src/2.4.3'
conv_file = os.path.join(exe_path, 'CONVBIN.exe')
post_file = os.path.join(exe_path, 'rnx2rtkp.exe')

# Setting Base extraction location
base_extract = os.path.splitext(base_zip)[0]
check_dir(base_extract)

# Extracting Base zip files
basezip = zipfile.ZipFile(base_zip, 'r')
basezip.extractall(base_extract)
basezip.close()

# Runnning base converter
run_base_converter = subprocess.Popen([conv_file,  os.path.join(
    base_extract, basename(base_extract)[:-4] + ".ubx"), "-r", "ubx", "-v", "3.03"])
run_base_converter.wait()

print(base_extract, base_extract[:-4] + ".ubx")

for rov in rover_zip:
    rover_extract = os.path.splitext(rov)[0]
    check_dir(rover_extract)
    roverzip = zipfile.ZipFile(rov, 'r')
    roverzip.extractall(rover_extract)
    roverzip.close()
    print(os.path.join(rover_extract, rover_extract[:-4] + ".ubx"))

    # Running rover converter
    run_rover_converter = subprocess.Popen([conv_file, os.path.join(
        rover_extract, basename(rover_extract)[:-4] + ".ubx"), "-r", "ubx", "-v", "3.03"])
    run_rover_converter.wait()

    # Running Post Processing
    # Rover Obs, Base Obs, nav, gnav, hnav, lnav, qnav, -c on -i on -h on

    if base_pos_prompt == 0:  # No position file is given
        run_rover_converter = subprocess.Popen([post_file, os.path.join(rover_extract, basename(rover_extract)[:-4] + ".obs"),
                                                os.path.join(base_extract, basename(
                                                    base_extract)[:-4] + ".obs"),
                                                os.path.join(base_extract, basename(
                                                    base_extract)[:-4] + ".nav"),
                                                "-o", os.path.join(rover_extract,
                                                                   basename(rover_extract)[:-4] + ".pos"),
                                                "-c", "on",
                                                "-h", "on",
                                                "-p", mode])

    if base_pos_prompt == 1:  # Position file is given
        run_rover_converter = subprocess.Popen([post_file, os.path.join(rover_extract, basename(rover_extract)[:-4] + ".obs"),
                                                os.path.join(base_extract, basename(
                                                    base_extract)[:-4] + ".obs"),
                                                os.path.join(base_extract, basename(
                                                    base_extract)[:-4] + ".nav"),
                                                "-o", os.path.join(rover_extract,
                                                                   basename(rover_extract)[:-4] + ".pos"),
                                                "-l", [base_position],
                                                "-c", "on",
                                                "-h", "on",
                                                "-p", mode])

    run_rover_converter.wait()

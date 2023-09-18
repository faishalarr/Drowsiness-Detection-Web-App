from tkinter import *
from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os
from plyer import notification
import pandas as pd

global saved
saved = "data/datrain"

def resize(directory):
    # Loop through all files in the directory
    for filename in os.listdir(directory):
            # Check if the file is a JPEG image
        if filename.lower().endswith((".jpg", ".jpeg")):
                # Open the image file
            filepath = os.path.join(directory, filename)
            image = Image.open(filepath)

                # Resize the image to fit within a 640x480 box
            image.thumbnail((640, 480))

                # Save the resized image with the same filename
            new_filepath = os.path.join("data", "datrain", filename)
            image.save(new_filepath)

def select_and_resize():
    lokasi = filedialog.askdirectory(parent=root,title="Select a directory")
    if lokasi:
        resize(lokasi)
    
root = tk.Tk()
root.withdraw()

select_and_resize()
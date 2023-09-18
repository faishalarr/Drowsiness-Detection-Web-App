import os
import shutil
import tkinter as tk
from tkinter import filedialog

def delete_directory(directory_path):
    if os.path.exists(directory_path):
        shutil.rmtree(directory_path)

def delete_files(directory_path):
    file_list = os.listdir(directory_path)
    for file_name in file_list:
        file_path = os.path.join(directory_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)

def move_files(file_paths, destination_directory):
    for file_path in file_paths:
        shutil.copy(file_path, destination_directory)

def select_directory():
    delete_directory("runs/detect/")  # Delete the directory

    directory_path = "data/images"
    delete_files(directory_path)  # Delete files in the directory
    
    detekinput_window = tk.Tk()
    detekinput_window.withdraw()  # Hide the main window
    
    

if __name__ == "__main__":
    select_directory()

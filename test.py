# Python Program to make a scrollable frame
# using Tkinter
  
import tkinter
import os
import main

image_folder="/home"

def rec_find_images(image_folder, masterlist):
    print(image_folder)
    # masterlist = [os.path.join(image_folder, file) for file in os.listdir(image_folder) if file.endswith(".png") or file.endswith(".jpg")]
    files = os.listdir(image_folder)
    for file in files:
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".PNG") or file.endswith(".JPG") or file.endswith(".JPEG") or file.endswith(".gif"):
            masterlist.append(os.path.join(image_folder, file))
        elif os.path.isdir(os.path.join(image_folder, file)):
            rec_find_images(os.path.join(image_folder, file), masterlist)
    return masterlist

images = rec_find_images(image_folder, [])

print(images)
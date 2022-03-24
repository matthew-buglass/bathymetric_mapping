import tkinter as tk
from tkinter import filedialog
from PIL import Image

"""
Script to calculate the approximate area of water (in km^2) in a given map 
with the basic colour scheme of a Google maps screenshot.

This is usefull because in the future, the user will be able to select a 
sample rate while on the water. By knowing an approximate area, the size
of the system's memory, and the size of the 3D model to print a user can
optimize their sample rate for hte accuracy that they need.
"""

# Open the google maps image
file = filedialog.askopenfilename(initialdir="C:\\",
                                  title="Select blue and green google image screenshot",
                                  filetypes=[("PNG files", "*.png")])
img = Image.open(file)

# Get the width and height in kms of the image.
width_km = float(input("What is the width in km of the image?   "))
height_km = float(input("What is the height in km of the image?   "))

# Get the number of pixels high and wide the image is.
img_width = img.width
img_height = img.height

# Calculate the square area per pixel in the image
km_per_width_pixel = width_km / img_width
km_per_height_pixel = height_km / img_height

sq_km_per_pixel = km_per_width_pixel * km_per_height_pixel

# Count the number of blue squares in the image
num_blue = 0
for w in range(img_width):
    for h in range(img_height):
        pixel = img.getpixel((w, h))
        if pixel == (156, 192, 249, 255):     # if the pixel is blue, we have water
            num_blue += 1

area = sq_km_per_pixel * num_blue

# Print the area to the console
print("The area of water in that image is: {:,.2f} square km".format(area))
print("The area of water in that image is: {:,.2f} square m".format(area * (1000**2)))


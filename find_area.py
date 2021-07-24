import tkinter as tk
from tkinter import filedialog
from PIL import Image

file = filedialog.askopenfilename(initialdir="D:\\",
                                  title="Select blue and green google image screenshot",
                                  filetypes=[("PNG files", "*.png")])
img = Image.open(file)

width_km = float(input("What is the width in km of the image?   "))
height_km = float(input("What is the height in km of the image?   "))

img_width = img.width
img_height = img.height

km_per_width_pixel = width_km / img_width
km_per_height_pixel = height_km / img_height

sq_km_per_pixel = km_per_width_pixel * km_per_height_pixel

num_blue = 0
for w in range(img_width):
    for h in range(img_height):
        pixel = img.getpixel((w, h))
        if pixel == (156, 192, 249, 255):     # if the pixel is blue, we have water
            num_blue += 1

area = sq_km_per_pixel * num_blue

print("The area of water in that image is: {:,.2f} square km".format(area))
print("The area of water in that image is: {:,.2f} square m".format(area * (1000**2)))


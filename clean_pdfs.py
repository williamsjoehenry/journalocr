# from pdf2image import convert_from_path
import os
from PIL import Image
import numpy as np

os.chdir("C:/Users/pithy/Documents/journalocr")

# for journal_no in [1,2,3]:
#     images = convert_from_path(f'data/{journal_no}.pdf')
#     for i, img in enumerate(images):
#         img.save(f'data/{journal_no}-{i}.jpg', 'JPEG')

def is_approximately_red(pixel):
    # Check if pixel falls within the red color range
    r, g, b = pixel
    return r - max(g, b) > 13

def get_reds(image):
    x_list = []
    y_list = []

    # Get image dimensions
    width, height = image.size

    # Iterate through each pixel
    for x in range(round(0.1*width), round(0.2*width)):
        for y in range(round(0.1*height), round(0.2*height)):
            pixel = image.getpixel((x, y))
            if is_approximately_red(pixel):
                x_list.append(x)
                y_list.append(y)
    
    return [x_list, y_list]

def rotate_page(image, angle):
    # TODO

# Example usage
input_image_path = "data/3-21.jpg"

# Flip the red pixels 90*, fit a line, check slope to measure verticality
coords = get_reds(Image.open(input_image_path))
line_of_best_fit = np.polyfit(coords[1], coords[0], 1)
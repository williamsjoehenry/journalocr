# from pdf2image import convert_from_path
import os
from PIL import Image
import numpy as np
import math

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
    top = []
    bottom = []

    # Get image dimensions
    width, height = image.size

    # Iterate through each pixel
    for x in range(round(0.1*width), round(0.3*width)):
        for y in range(round(0.1*height), round(0.15*height)):
            pixel = image.getpixel((x, y))
            if is_approximately_red(pixel):
                top.append(x)

    # Iterate through each pixel
    for x in range(round(0.1*width), round(0.3*width)):
        for y in range(round(0.8*height), round(0.85*height)):
            pixel = image.getpixel((x, y))
            if is_approximately_red(pixel):
                bottom.append(x)
    return [top, bottom]

def rotate_page(image):
    before = get_reds(image)

    top_mean = np.mean(before[0])
    bottom_mean = np.mean(before[1])

    _, height = image.size

    top = 0.15*height
    bottom = 0.85*height

    slope = (top - bottom) / (top_mean - bottom_mean)

    angle = math.degrees(math.atan(slope)) + 90

    return image.rotate(angle, resample = Image.BICUBIC, expand = True).show()

def split_lines(image):
    width, height = image.size
    for row in range(height):
        pixels = list(image.getdata())[row * width: (row + 1) * width]
        row_avg = np.mean(pixels)
        print(row, row_avg)
    return row_avg
    # img_array = np.array(image, dtype=np.uint8)
    # return(img_array)

# Example usage
input_image_path = "data/2-138.jpg"
test_image = Image.open(input_image_path)
width, height = test_image.size
split_lines(test_image)
# rotate_page(test_image)
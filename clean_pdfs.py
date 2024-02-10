from pdf2image import convert_from_path
import os
from PIL import Image
import numpy as np
import math

os.chdir("C:/Users/pithy/Documents/journalocr")

def is_red(pixel):
    # Check if pixel falls within the red color range
    r, g, b = pixel
    return r - max(g, b) > 10

def get_reds(image_path):
    image = Image.open(image_path).convert('RGB')
    top = []
    bottom = []

    # Get image dimensions
    width, height = image.size

    # Iterate through each pixel
    for x in range(round(0.1*width), round(0.3*width)):
        for y in range(round(0.1*height), round(0.15*height)):
            pixel = image.getpixel((x, y))
            if is_red(pixel):
                top.append(x)

    # Iterate through each pixel
    for x in range(round(0.1*width), round(0.3*width)):
        for y in range(round(0.8*height), round(0.85*height)):
            pixel = image.getpixel((x, y))
            if is_red(pixel):
                bottom.append(x)
    return [top, bottom]

def is_blue(pixel):
    # Check if pixel is blue or green (lines sometimes greenish blue on the scan)
    r, g, b = pixel
    return min(g, b) - r > 4

def get_blues(image):
    # image = Image.open(image_path).convert('RGB')
    l1 = []
    r1 = []
    l2 = []
    r2 = []

    # Get image dimensions
    width, height = image.size
    first_line = round(height * 1.125/9.75)
    second_line = round(height * (1.125 + 0.3125)/9.75)

    # Iterate through each pixel
    for x in range(round(0.1*width), round(0.3*width)):
        for y in range(first_line - 20, first_line + 20):
            pixel = image.getpixel((x, y))
            if is_blue(pixel):
                l1.append((x, y))
    for pixel in l1:
        x, y = pixel
        image.putpixel((x,y), (0, 0, 255))

    # Iterate through each pixel
    for x in range(round(0.1*width), round(0.3*width)):
        for y in range(second_line - 20, second_line + 20):
            pixel = image.getpixel((x, y))
            if is_blue(pixel):
                l2.append((x, y))
    for pixel in l2:
        x, y = pixel
        image.putpixel((x,y), (0, 0, 255))

    image.show()


def crop_top(image, width, height):
    # Check brightness at top of page on the left and right ends
    left_bright = np.mean(np.array(image.convert('L').crop((100, 0, 150, 10))))
    right_bright = np.mean(np.array(image.convert('L').crop((width-150, 0, width-100, 10))))

    # If the top of the page is white on both halves, you're done
    if left_bright > 200 and right_bright > 200:
        return(image)

    # Chop a little off the top and try again
    image = image.crop((0, 10, width, height))
    return crop_top(image, width, height)

def rotate_and_cleave_page(image_path):
    # Open image
    image = Image.open(image_path).convert('RGB')

    # Rotate to vertical
    before = get_reds(image_path)
    top_mean = np.mean(before[0])
    bottom_mean = np.mean(before[1])

    width, height = image.size
    top = round(0.15*height)
    bottom = round(0.85*height)

    if round(top_mean) - round(bottom_mean) > 3:
        slope = (top - bottom) / (top_mean - bottom_mean)
        angle = math.degrees(math.atan(slope)) + 90

        image = image.rotate(angle, resample = Image.BICUBIC, expand = True)

    # Trim the top of the page to remove any black from poor scan/rotation
    image = crop_top(image, width, height)

    # draw = ImageDraw.Draw(image).line((0, height*(1.125/9.75), width, height*(1.125/9.75)), fill = 'red', width = 1)
    # image.show()
    get_blues(image)

    # split rotated image and save sidebar and body text
    split_point = np.mean(get_reds(image_path)[0])
    sidebar = image.crop(box = (0, 0, split_point, height))
    body = image.crop(box = (split_point, 0, width, height))
    # sidebar.show(); body.show()

    # split_lines(sidebar)
    # split_lines(body)
    
    # sidebar.save(f'{image_path[0:-4]}-s.jpg')
    # body.save(f'{image_path[0:-4]}-b.jpg')


# Example usage
from PIL import ImageDraw
input_image_path = "data/2-120.jpg"
rotate_and_cleave_page(input_image_path)
# test_image = Image.open(input_image_path).convert('RGB')
# crop_top(test_image)

# for journal_no in [1,2,3]:
#     images = convert_from_path(f'data/{journal_no}.pdf')
#     for i, img in enumerate(images):
#         # TODO: consider refactoring image/path so that you don't need to save the intact pages as intermediaries?
#         img.save(f'data/{journal_no}-{i}.jpg', 'JPEG')
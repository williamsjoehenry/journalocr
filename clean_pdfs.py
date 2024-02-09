from pdf2image import convert_from_path
import os

os.chdir("C:/Users/pithy/Documents/journalocr")

for journal_no in [1,2,3]:
    images = convert_from_path(f'data/{journal_no}.pdf')
    for i, img in enumerate(images):
        img.save(f'data/{journal_no}-{i}.jpg', 'JPEG')
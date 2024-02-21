from PIL import Image
from random import randint
from os import listdir, chdir

chdir("Documents/journalocr")

while True:
    filename = f"data/lines/{randint(1,3)}-{randint(14, 151)}-{randint(0, 20)}.jpeg"
    with Image.open(filename) as img:
        img.convert('RGB').show()
    label = input(">")
    with open("fine_tune_examples.txt", "a") as out:
        out.write(filename+' '+label+'\n')
    out.close()
    img.close()
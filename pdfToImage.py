import os
from pdf2image import convert_from_path

ROOT = './documents/'

idx = 1

for file in os.listdir(ROOT):
    images = convert_from_path(os.path.join(ROOT, file), poppler_path=r'C:\Users\mikol\Downloads\poppler-22.04.0\Library\bin')
    image0 = images[0]
    image1 = images[1]
    image0.save(f'./images/image_{idx}_0.png')
    image1.save(f'./images/image_{idx}_1.png')
    idx += 1

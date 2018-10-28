#!/usr/bin/env python3
import argparse
import pytesseract
import sys
from PIL import Image

parser = argparse.ArgumentParser(description='Converts images to readable ASCII')

parser.add_argument('-p', '--psm', type=int, metavar='', help='Config PSM')

parser.add_argument('-f', '--file', type=str, metavar='', required=True, help='image file')

arguments = parser.parse_args()

image = Image.open(arguments.file).convert('1')

text = ''

if arguments.psm: 
	text = pytesseract.image_to_string(image, config='--psm {}'.format(arguments.psm))
else:
	text = pytesseract.image_to_string(image)
 
print(text)

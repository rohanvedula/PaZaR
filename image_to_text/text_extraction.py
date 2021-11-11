"""
import pytesseract
from pytesseract import pytesseract as pt
import shutil
import os
import random
try:
 from PIL import Image
except ImportError:
 import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
print(pytesseract.image_to_string(r'D:\examplepdf2image.png'))

"""


import cv2
import pytesseract
from pytesseract import Output
import csv


image = cv2.imread('images/test9.png')

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


#cv2.imshow('threshold image',  threshold_img)

custom_config = r'--oem 3 --psm 6'


details = pytesseract.image_to_data(threshold_img, output_type=Output.DICT, config=custom_config, lang='eng')

print(details.keys())

total_boxes = len(details['text'])



for sequence_number in range(total_boxes):

    if int(details['conf'][sequence_number]) >40 and details['text'][sequence_number].isnumeric()==False:
        (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
        threshold_img = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

    else:
        print("")

parse_text = []
word_list = []
last_word = ''

for word in details['text']:

    if word!='':
        word_list.append(word)
        last_word = word

    if (last_word!='' and word == '') or (word==details['text'][-1]):
        parse_text.append(word_list)
        word_list = []

#print(word_list)

with open('result_text.txt',  'w', newline="") as file:
    csv.writer(file, delimiter=" ").writerows(parse_text)

cv2.imshow('captured text', threshold_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

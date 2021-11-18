import cv2
import pytesseract
from pytesseract import Output
import csv, os
import numpy as np
from urllib.request import urlopen

def extract_text(url):
    image_path = urlopen(url) # os.path.join(os.path.dirname(__file__), "images", "test9.png")

    image = np.asarray(bytearray(image_path.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    #image = cv2.imread(image_path.read())
    dimensions = image.shape

    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    print(dimensions)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


    threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


    #cv2.imshow('threshold image',  threshold_img)

    custom_config = r'--oem 3 --psm 6'


    details = pytesseract.image_to_data(threshold_img, output_type=Output.DICT, config=custom_config, lang='eng')

    print(details.keys())

    total_boxes = len(details['text'])
    special_characters = "!@#$%^&*()-+?_=,<>/"

    #int(details['conf'][sequence_number]) >40 and 

    for sequence_number in range(total_boxes):

        if details['text'][sequence_number].isalnum()==False:
            (x, y, w, h) = (details['left'][sequence_number], details['top'][sequence_number], details['width'][sequence_number],  details['height'][sequence_number])
            area = (w*h)/(dimensions[0]*dimensions[1])
            add = int((dimensions[0]*dimensions[1])*0.0001)
            #or any(c in special_characters for c in details['text'][sequence_number])
            if(area<0.0017):
                crop = image[y:y+h, x:x+w]
                cv2.imshow('Image', crop) #shows the image can be removed and API call can be placed here or we can make an array and call the symbol recognizer API like that
                cv2.waitKey(0) 
                threshold_img = cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

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

    print(word_list)

    return word_list

    # with open('result_text.txt',  'w', newline="") as file:
    #     csv.writer(file, delimiter=" ").writerows(parse_text)

    # cv2.imshow('captured text', threshold_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

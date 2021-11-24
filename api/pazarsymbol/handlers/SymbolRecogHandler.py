from flask import redirect
from flask_restful import Api, Resource, reqparse
import json, os
from .symbol_recognition import identify as symbol_classifier
import numpy as np


class SymbolRecogHandler(Resource):
    def get(self):
        return {
            "message": "Success"
        }
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("image_array", type=str)

        args = parser.parse_args()

        text_list = args['image_array']

        image_list = text_list.split("?")
        image_list = [temp_list.split("~") for temp_list in image_list]
        image_list = [[temp_string.split("#") for temp_string in temp_list]for temp_list in image_list]

        for i, a in enumerate(image_list):
            for j, b in enumerate(a):
                for k, c in enumerate(b):
                    image_list[i][j][k] = int(c)

        numpy_image = np.array(image_list, dtype=np.uint8)

        # print(numpy_image)
        # print("Shape: " + str(numpy_image.shape))

        processed_img, results = symbol_classifier.identify(numpy_image, 1)
        
        # print(result)
        results = results[0]
        true_results = (str(results[0]), results[1])

        return {
            "result" : true_results
        }

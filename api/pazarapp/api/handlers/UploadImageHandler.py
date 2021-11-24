from flask import redirect
from flask_restful import Api, Resource, reqparse
import json, os
from .text_extraction import extract_text
from .to_latex_code import to_latex_code

class UploadImageHandler(Resource):
    def get(self):
        return {
            "message": "Success"
        }
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("image_url", type=str)

        args = parser.parse_args()

        text_list = extract_text(args['image_url'])

        text = to_latex_code(text_list)

        return {
            "text" : text
        }

        
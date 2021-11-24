import cloudinary.uploader, json, os, requests
from dotenv import load_dotenv
from text_to_latex import create_document, append_text
import os

def upload_image(path):
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    cloudinary.config(cloud_name='guptap1',
                  api_key=os.environ.get("API_KEY"),
                  api_secret=os.environ.get("API_SECRET"))
    response = cloudinary.uploader.upload(path, folder="pazar/")
    return response["url"]

def send_uploaded(url):
    response = requests.post("https://pazarapp.herokuapp.com/upload", data={"image_url" : url})
    return response.json()['text']

latex_code = send_uploaded(upload_image(os.path.join(os.path.dirname(__file__), 'sample_images', 'test9.png')))

# find path of test_documents directory
path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'test_documents', 'test_api')

# create test document
doc = create_document("My Math Notes", path)

print(latex_code)

# append string to test document
append_text(doc, latex_code)
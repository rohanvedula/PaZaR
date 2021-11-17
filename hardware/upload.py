import cloudinary.uploader, json, os
from dotenv import load_dotenv

def upload_image(path):
    load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
    cloudinary.config(cloud_name='guptap1',
                  api_key=os.environ.get("API_KEY"),
                  api_secret=os.environ.get("API_SECRET"))
    response = cloudinary.uploader.upload(path, folder="pazar/")
    print(response["url"])

# upload_image(os.path.join(os.path.dirname(__file__), 'sample_images', 'image20.jpg'))
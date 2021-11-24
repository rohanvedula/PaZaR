from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from handlers.SymbolRecogHandler import SymbolRecogHandler

app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route("/")
def serve():
    return {"message" : "Hi there" }

api.add_resource(SymbolRecogHandler, "/upload")

if __name__ == '__main__':
    app.run(port=5001)
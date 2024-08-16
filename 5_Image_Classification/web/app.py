from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import numpy as np
import requests

# from keras_applications import inception_v3
# from keras_applications.inception_v3 import preprocess_input
# from keras_applications import imagenet_utils
# from tensorflow.keras.preprocessing.image import img_to_array
# from PIL import Image
# from io import BytesIO

from keras.applications import InceptionV3
from keras.applications.inception_v3 import preprocess_input
from keras.applications import imagenet_utils
from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
from io import BytesIO

app = Flask(__name__)
api = Api(app)

pretrained_model = InceptionV3(weights="imagenet") # Load the pre trained model

client = MongoClient("mongodb://db:27017") # Initialize MongoClient
db = client.ImageRecognition # Create a new db and collection
users = db["Users"]
InitialTokens = 6

class AppUtils():
    def userExists(username):
        if users.count_documents({"Username":username}) == 0:
            return False
        return True

class Register(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        if AppUtils.userExists(username):
            return jsonify({"status":301,"message":"Invalid username, user already exists"})
        
        hashedPW = bcrypt.hashpw(password.encode('utf8'),bcrypt.gensalt())
        users.insert_one({"Username":username, "Password":hashedPW, "Tokens":InitialTokens})

        return jsonify({"status":200,"message":"You have successfully signed up for the API"})
    

class Classify(Resource):
    def post(self):
        #Get posted data
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        url = postedData["url"]
        # Get credential and url
        # verify credentials
        # check for tokens
        # classify the image
        # return classification response

api.add_resource(Register, '/register')
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import numpy as np
import requests

# from keras.applications import InceptionV3
# from keras.applications.inception_v3 import preprocess_input
# from keras.applications import imagenet_utils
# from tensorflow.keras.preprocessing.image import img_to_array
from PIL import Image
from io import BytesIO

app = Flask(__name__)
api = Api(app)

# pretrained_model = InceptionV3(weights="imagenet") # Load the pre trained model

client = MongoClient("mongodb://db:27017") # Initialize MongoClient
db = client.ImageRecognition # Create a new db and collection
users = db["Users"]
InitialTokens = 6
correctAdminPW = "abc123"

class AppUtils():
    def userExists(username):
        if users.count_documents({"Username":username}) == 0:
            return False
        return True

    def genReturnJson(status, msg):
        return {"status":status,"msg":msg}
    
    def verifyPW(username, password):
        if not AppUtils.userExists(username):
            return False
        
        hashedPW = users.find({"Username":username})[0]["Password"]

        if bcrypt.hashpw(password.encode('utf8'), hashedPW) == hashedPW:
            return True
        
        return False
    
    def verifyCredentials(username, password):
        if not AppUtils.userExists(username):
            return AppUtils.genReturnJson(301, "Invalid Username"), True
        
        if not AppUtils.verifyPW(username, password):
            return AppUtils.genReturnJson(302, "Invalid Password"), True
        
        return None, False

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
        #Get posted data then credentials and url
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        url = postedData["url"]

        # verify 
        retJson, error = AppUtils.verifyCredentials(username, password)
        if error:
            return jsonify(retJson)
        
        # check for tokens
        tokens = users.find({"Username":username})[0]["Tokens"]
        if tokens <= 0:
            return jsonify(AppUtils.genReturnJson(303, "Not Enough Tokens"))
        
        if not url: 
            return jsonify(({"error":"No Url provided"}),400)
        
        # Load image from URL
        response = requests.get(url) # download user image from url as a file
        img = Image.open(BytesIO(response.content)) # open the image file
        
        # Pre process the image
        # img = img.resize((299,299))
        # imgArray = img_to_array(img) # convert to numpy number array
        # imgArray = np.expand_dims(imgArray, axis=0) # set axis
        # imgArray = preprocess_input(imgArray)

        # # Make prediction
        # prediction = pretrained_model.predict(imgArray)
        # actualPrediction = imagenet_utils.decode_predictions(prediction, top=5)

        # return classification response
        retJson = {"her":"hey"}
        # retJson = {}
        # for pred in actualPrediction[0]:
        #     retJson[pred[1]] = float(pred[2]*100)
        
        #reduce token
        tokens -= 1
        users.update_one({"Username":username},{"$set":{"Tokens":tokens}})

        return jsonify(retJson)


        


class Refill(Resource):
    def post(self):
        #Get posted data then credentials and url
        postedData = request.get_json()
        username = postedData["username"]
        adminPW = postedData["adminPW"]
        amount = postedData["amount"]

        # verify 
        if not AppUtils.userExists(username):
            return jsonify({"status":301,"message":"Invalid username, user doesnt exists"})
        
        if not adminPW == correctAdminPW:
            return jsonify({"status":302,"message":"Invalid password"})
        
        # update tokens
        users.update_one({"Username":username},{"$set":{"Tokens":amount}})
        
        return AppUtils.genReturnJson(200, "Tokens refilled to amount asked")
    


api.add_resource(Register, '/register')
api.add_resource(Classify, '/classify')
api.add_resource(Refill, '/refill')


if __name__ == '__main__':
    app.run(host='0.0.0.0')

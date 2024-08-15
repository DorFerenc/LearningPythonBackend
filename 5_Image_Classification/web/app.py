from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import numpy as np
import requests

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.ImageRecognition
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


api.add_resource(Register, '/register')
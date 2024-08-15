"""
Register of a user 0 tokens
Each user gets 10 tokens
Store a sentence on our database for 1 token
Retrive his stored sentence on out database for 1 token
"""

from flask import Flask, jsonify, request
from flask_restful import Api, Resource
import bcrypt
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]

initial_tokens = 6

class MyWebUtils():
    def verifyPw(username, password):
        hashed_pw = users.find({"Username":username})[0]["Password"]
        if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
            return True
        return False

    def countTokens(username):
        return users.find({"Username":username})[0]["Tokens"]

class Register(Resource):
    def post(seld):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        users.insert_one({"Username": username,"Password": hashed_pw,"Sentence": "","Tokens": initial_tokens})

        return jsonify({"status":200,"msg":"You have successfully signed up for the API"})

class Store(Resource):
    def post(self):
        postedData = request.get_json()
        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        correct_pw = MyWebUtils.verifyPw(username, password)
        if not correct_pw:
            return jsonify({"status":302,"msg":"Invalid Username passowrd combination"})

        num_tokens = MyWebUtils.countTokens(username)
        if num_tokens <= 0:
            return jsonify({"status":301,"msg":"Out of tokens"})
        
        users.update_one({"Username": username},{"$set":{"Sentence":sentence,"Tokens":num_tokens-1}})

        return jsonify({"status":200,"msg":f"Sentence saved successfully {num_tokens} left"})

class Get(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        correct_pw = MyWebUtils.verifyPw(username, password)
        if not correct_pw:
            return jsonify({"status":302,"msg":"Invalid Username passowrd combination"})
        
        num_tokens = MyWebUtils.countTokens(username)
        if num_tokens <= 0:
            return jsonify({"status":301,"msg":"Out of tokens"})
        
        users.update_one({"Username": username},{"$set":{"Tokens":num_tokens-1}})
        
        sentence = users.find({"Username":username})[0]["Sentence"]
        return jsonify({"status":200,"msg":f"Sentence: {sentence}, {num_tokens} left"})


api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
        



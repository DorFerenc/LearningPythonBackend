from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db["Users"]

initialTokens = 6
correctAdminPw = "abc123"


class AppUtils():
    def userExists(username):
        if users.count_documents({"Username":username}) == 0:
            return False
        return True
    
    def verifyPassword(username, password):
        if not AppUtils.userExists(username):
            return False
        hashedPW = users.find({"Username":username})[0]["Password"]
        if not bcrypt.hashpw(password.encode('utf8'), hashedPW) == hashedPW:
            return False
        return True
    
    def countTokens(username):
        return (users.find({"Username":username})[0]["Tokens"])


class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        if AppUtils.userExists(username):
            return jsonify({"status":301, "msg":"Invalid Username"})

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert_one({"Username": username, "Password":hashed_pw, "Tokens": initialTokens})

        return jsonify({"status":200, "msg":"You've successfully signed up to the API"})


class Detect(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        text1 = postedData["text1"]
        text2 = postedData["text2"]

        if not AppUtils.userExists(username):
            return jsonify({"status":301, "msg":"Invalid Username"})
        
        if not AppUtils.verifyPassword(username, password):
            return jsonify({"status":302, "msg":"Invalid passowrd"})

        numTokens = AppUtils.countTokens(username)
        if numTokens <= 0:
            return jsonify({"status":303, "msg":"Out of tokens"})

        nlp = spacy.load('en_core_web_sm')
        text1 = nlp(text1)
        text2 = nlp(text2)
        ratioOfSimilarity = text1.similarity(text2) # Number between 0 and 1 | Closer to 1 = more similar

        users.update_one({"Username":username},{"$set":{"Tokens":numTokens-1}})

        return jsonify({"status":200, "similarity":ratioOfSimilarity, "msg": f"Similarity score calculated successfully you have {numTokens-1} left"})

class Refill(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        adminPW = postedData["adminPW"]
        refillAmount = postedData["refillAmount"]

        if not AppUtils.userExists(username):
            return jsonify({"status":301, "msg":"Invalid Username"})
        
        if adminPW != correctAdminPw:
            return jsonify({"status":304, "msg":"Invalid Admin Password"})
        
        currentTokens = AppUtils.countTokens(username)
        users.update_one({"Username":username},{"$set":{"Tokens":currentTokens + refillAmount}})

        return jsonify({"status":200, "msg": f"Refilled successfully you have {currentTokens + refillAmount} left"})
    
api.add_resource(Register, '/register')
api.add_resource(Detect, '/detect')
api.add_resource(Refill, '/refill')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
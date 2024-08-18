from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.BankAPI
users = db["Users"]

transactionFee = 1
correctAdminPw = "abc123"


class AppUtils():
    def userExists(username):
        if users.count_documents({"Username":username}) == 0:
            return False
        return True
    
    def verifyCredentials(username, password):
        if not AppUtils.userExists(username):
            return AppUtils.generateReturnJson(301,"Invalid Username"), True
        hashedPW = users.find({"Username":username})[0]["Password"]
        if not bcrypt.hashpw(password.encode('utf8'), hashedPW) == hashedPW:
            return AppUtils.generateReturnJson(302,"Invalid Password"), True
        return None, False
    
    def getUserCash(username):
        return (users.find({"Username":username})[0]["Own"])
    
    def getUserDept(username):
        return (users.find({"Username":username})[0]["Dept"])
    
    def generateReturnJson(status, msg):
        return jsonify({"status":status,"msg":msg})
    
    def updateAcountBalance(username, balance):
        users.update_one({"Username":username}, {"$set":{"Own":balance}})
    
    def updateAcountDept(username, balance):
        users.update_one({"Username":username}, {"$set":{"Dept":balance}})


class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        if AppUtils.userExists(username):
            return AppUtils.generateReturnJson(301,"Invalid Username")

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert_one({"Username": username, "Password":hashed_pw, "Own": 0, "Debt": 0})

        return AppUtils.generateReturnJson(200,"You've successfully signed up to the API")


class Add(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        amount = postedData["amount"]

        retJson, error = AppUtils.verifyCredentials(username, password)
        if error: 
            return retJson
        
        if amount <= 0:
            return AppUtils.generateReturnJson(304, "The money amount entered must be >0")

        currentUserCash = AppUtils.getUserCash(username)
        bankCash = AppUtils.getUserCash("BANK") # check how mush cash the bank has
        currentUserCash -= transactionFee # Take a tranaction fee from the user
        AppUtils.updateAcountBalance("BANK", bankCash + transactionFee)
        AppUtils.updateAcountBalance(username, currentUserCash + amount)

        return AppUtils.generateReturnJson(200, "Amount added succesfully")
        
class Transfer(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        to = postedData["to"]
        amount = postedData["amount"]

        retJson, error = AppUtils.verifyCredentials(username, password)
        if error: 
            return retJson
        
        currentUserCash = AppUtils.getUserCash(username)
        if currentUserCash <= 0:
            return AppUtils.generateReturnJson(304, "You are out of money please get amount")
        
        if not AppUtils.userExists(to):
            return AppUtils.generateReturnJson(301, "Reciever Username is invalid")

        reciverUserCash = AppUtils.getUserCash(to)
        bankCash = AppUtils.getUserCash("BANK")

        AppUtils.updateAcountBalance(username, reciverUserCash - amount - transactionFee)
        AppUtils.updateAcountBalance(to, reciverUserCash + amount)
        AppUtils.updateAcountBalance("BANK", bankCash + transactionFee)

        return AppUtils.generateReturnJson(200, "Amount transfered succesfully")


class Balance(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        retJson, error = AppUtils.verifyCredentials(username, password)
        if error: 
            return retJson

        return jsonify(users.find({"Username":username},{"Password":0, "_id":0})[0])


class TakeLoan(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        amount = postedData["amount"]

        retJson, error = AppUtils.verifyCredentials(username, password)
        if error: 
            return retJson
        
        if amount <= 0:
            return AppUtils.generateReturnJson(304, "The money amount entered must be >0")
        
        currentUserCash = AppUtils.getUserCash(username)
        currentUserDebt = AppUtils.getUserDept(username)
        AppUtils.updateAcountDept(username, currentUserDebt + amount)
        AppUtils.updateAcountBalance(username, currentUserCash + amount)

        return AppUtils.generateReturnJson(200, "Loan added to your account")


class PayLoan(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        amount = postedData["amount"]

        retJson, error = AppUtils.verifyCredentials(username, password)
        if error: 
            return retJson
        
        if amount <= 0:
            return AppUtils.generateReturnJson(304, "The money amount entered must be >0")
        
        currentUserCash = AppUtils.getUserCash(username)

        if currentUserCash < amount:
            return AppUtils.generateReturnJson(303, "Not enough cash in your account to pay this amount")
        
        currentUserDebt = AppUtils.getUserDept(username)
        AppUtils.updateAcountBalance(username, currentUserCash - amount)
        AppUtils.updateAcountDept(username, currentUserDebt - amount)

        return AppUtils.generateReturnJson(200, "You've succesfully paid the amount off your loan")
    

api.add_resource(Register, '/register')
api.add_resource(Add, '/add')
api.add_resource(Transfer, '/transfer')
api.add_resource(Balance, '/balance')
api.add_resource(TakeLoan, '/takeloan')
api.add_resource(PayLoan, '/payloan')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
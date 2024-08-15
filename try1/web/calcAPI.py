from flask import Flask, jsonify, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

def checkPostedData(postedData, functionName):
    if "x" not in postedData or "y" not in postedData:
        return 301

    if functionName == "divide":
        if int(postedData["y"]) == 0:
            return 302
    
    return 200

class Add(Resource):
    def post(self):
        #If I am here, then the resource Add was requested using the method POST
        #Step 1: Get poseted data:
        postedData = request.get_json()

        #Step 1b: Verify validity of posted datat
        status_code = checkPostedData(postedData, "add")
        if (status_code != 200):
            retJson = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return jsonify(retJson)

        x = int(postedData["x"])
        y = int(postedData["y"])

        #Step 2: Add the posted data
        res = x + y
        resMap = {
            'Message': (res),
            'Status Code': 200
        }

        #Step 3: Return the message to the user
        return jsonify(resMap)

class Subtract(Resource):
    def post(self):
        postedData = request.get_json()

        status_code = checkPostedData(postedData, "subtract")
        if (status_code != 200):
            retJson = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return jsonify(retJson)

        x = int(postedData["x"])
        y = int(postedData["y"])

        res = x - y
        resMap = {
            'Message': (res),
            'Status Code': 200
        }
        return jsonify(resMap)

class Multiply(Resource):
    def post(self):
        postedData = request.get_json()

        status_code = checkPostedData(postedData, "multiply")
        if (status_code != 200):
            retJson = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return jsonify(retJson)

        x = int(postedData["x"])
        y = int(postedData["y"])

        res = x * y
        resMap = {
            'Message': (res),
            'Status Code': 200
        }
        return jsonify(resMap)

class Divide(Resource):
    def post(self):
        postedData = request.get_json()

        status_code = checkPostedData(postedData, "divide")
        if (status_code != 200):
            retJson = {
                "Message": "An error happened",
                "Status Code": status_code
            }
            return jsonify(retJson)

        x = int(postedData["x"])
        y = int(postedData["y"])

        res = (x * 1.0) / y
        resMap = {
            'Message': (res),
            'Status Code': 200
        }
        return jsonify(resMap)

#Add resources to the api
api.add_resource(Add, "/add")
api.add_resource(Subtract, "/subtract")
api.add_resource(Multiply, "/multiply")
api.add_resource(Divide, "/divide")


@app.route('/')
def hello_world():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0')
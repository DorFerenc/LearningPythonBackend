# from flask import Flask, jsonify, request

# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return "Hello World!"

# @app.route('/hithere')
# def hi_there_everyone():
#     return "I just hit /hithere"

# @app.route('/add_two_nums', methods=["POST"])
# def add_two_nums():
#     #Get x,y from the posted data
#     dataDict = request.get_json()

#     #add checks
#     if "x" not in dataDict or "y" not in dataDict:
#         return "ERROR", 305
#     x = dataDict["x"]
#     y = dataDict["y"]
#     #Add z = x+y
#     z = x+y
#     #Prepare a JSON "z":z
#     resJSON = {
#         "z":z
#     }
#     #return jsonify(map_prepared)
#     return jsonify(resJSON), 2001

# @app.route('/bye')
# def bye():
#     c = 2*534
#     s=str(c)
#     c = 1/0
#     return "bye" + s

# if __name__ == "__main__":
#     app.run(debug=True)
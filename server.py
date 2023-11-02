from flask import Flask
from flask import request, jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    print("hello")
    return "<p>Hello, World!</p>"

@app.route('/db', methods = ['POST'])
def get_data():

    ##Send SQL query - TODO

    ##Parse SQL query and Send JSON object back with x and y data for graph - TODO
    data = dict()
    data['x']=[1,2,3,4,5]
    data['y']=[1,2,3,4,5]
    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=data),200
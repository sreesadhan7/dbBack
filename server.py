from flask import Flask
from flask import request, jsonify
import oracledb
import queries as q
app = Flask(__name__)
cs = "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=oracle.cise.ufl.edu)(PORT=1521))(CONNECT_DATA=(SERVER=DEDICATED)(SID=orcl)))"
connection = oracledb.connect(
user='golamari.h',
password='rWd2BmKUUyF67AJDP7cZ0ecY',
dsn=cs)

cursor = connection.cursor()
print("Successfully connected to Oracle Database")

@app.route("/")
def hello_world():
    print("hello")
    return "<p>Hello, World!</p>"

@app.route('/db', methods = ['POST'])
def get_data():

    ##Send SQL query - TODO

    ##Connection to db

    # ##Query
    res = cursor.execute(q.mockup_1_1.format('Afghanistan', 5, 1960, 2022))
    
    for row in res:
        if (row[1]):
            print(row[0], "is done")
        else:
            print(row[0], "is NOT done")

    ##Parse SQL query and Send JSON object back with x and y data for graph - TODO
    data = dict()
    data['x']=[1,2,3,4,5]
    data['y']=[1,2,3,4,5]
    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=data),200
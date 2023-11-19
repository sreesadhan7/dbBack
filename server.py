from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
import oracledb
import queries as q
app = Flask(__name__)
CORS(app)
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
    data = request.get_json()
    print(data)
    ##Connection to db
    
    year_dict = {"Y":1, "2Y":2, "3Y":3, "5Y":5}


    # ##Query
    res = cursor.execute(q.mockup_1_1.format(data["country"], year_dict[data["agg"]], data['from'], data['to']))
    
    data_db = dict()
    data_db['x']=[]
    data_db['y1']=[]
    data_db['y2']=[]
    for row in res:
        data_db['x'].append(row[0])
        data_db['y1'].append(row[2])
        data_db['y2'].append(row[1])


    ##Parse SQL query and Send JSON object back with x and y data for graph - TODO

    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=data_db),200
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

@app.route('/mockup_1_1', methods = ['POST'])
def get_data():
    print("server   SERVER HIT")
    ##Send SQL query - TODO
    data = request.get_json()
    year_dict = {"Y":1, "2Y":2, "3Y":3,"4Y":4, "5Y":5}
    # ##Query
    res = cursor.execute(q.mockup_1_1.format(data["country"], year_dict[data["agg"]], data['from'], data['to']))
    #res = cursor.execute(q.mockup_1_1.format("India", 1, 2000, 2021))
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
    
    
@app.route('/mockup_1_2', methods = ['POST'])
def get_data1_2():

    #mockup_1_2 doesnt have any parameters
    ##Send SQL query - TODO
    # data = request.get_json()
    # ##Query
    res = cursor.execute(q.mockup_1_2)
    
    data_db = dict()
    data_db['x']=[]
    data_db['y1']=[]
    for row in res:
        data_db['x'].append(row[0])
        data_db['y1'].append(row[1])

    ##Parse SQL query and Send JSON object back with x and y data for graph - TODO

    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=data_db),200
    

    
@app.route('/mockup_1_3', methods = ['POST'])
def get_data1_3():

    #mockup_1_2 doesnt have any parameters
    ##Send SQL query - TODO
    data = request.get_json()
    # ##Query
    res = cursor.execute(q.mockup_1_3.format(data["country"],  data['from'], data['to']))
    
    data_db = dict()
    data_db['x']=[]
    data_db['y1']=[]
    data_db['y2']=[]
    data_db['y3']=[]
    data_db['y4']=[]
    for row in res:
        data_db['x'].append(row[0])
        data_db['y1'].append(row[1])
        data_db['y2'].append(row[2])
        data_db['y3'].append(row[3])
        data_db['y4'].append(row[4])
    ##Parse SQL query and Send JSON object back with x and y data for graph - TODO

    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=data_db),200
    
    
@app.route('/mockup_2_1', methods = ['POST'])
def get_data2_1():

    #mockup_1_2 doesnt have any parameters
    ##Send SQL query - TODO
    data = request.get_json()
    # ##Query
    res = cursor.execute(q.mockup_2_1.format(data["top_n_countries"],  data['from'], data['to']))
    
    data_db = dict()
    data_db['x']=[]
    data_db['y1']=[]
    data_db['y2']=[]
    
    for row in res:
        data_db['x'].append(row[0])
        data_db['y1'].append(row[1])
        data_db['y2'].append(row[2])

    ##Parse SQL query and Send JSON object back with x and y data for graph - TODO

    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=data_db),200
    
@app.route('/mockup_2_2', methods = ['POST'])
def get_data2_2():

    #mockup_1_2 doesnt have any parameters
    ##Send SQL query - TODO
    data = request.get_json()
    # ##Query
    res = cursor.execute(q.mockup_2_2.format(data["country"],  data['from'], data['to']))
    
    
    data_db = dict()
    data_db['x']=[]
    data_db['y1']=[]
    data_db['y2']=[]
    data_db['y3']=[]
    
    for row in res:
        data_db['x'].append(row[0])
        data_db['y1'].append(row[1])
        data_db['y2'].append(row[2])
        data_db['y3'].append(row[3])

    ##Parse SQL query and Send JSON object back with x and y data for graph - TODO

    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=data_db),200
    
@app.route('/mockup_2_3', methods = ['POST'])
def get_data2_3():

    #mockup_1_2 doesnt have any parameters
    ##Send SQL query - TODO
    data = request.get_json()
    # ##Query
    res = cursor.execute(q.mockup_2_3.format(data["country"],  data['from'], data['to']))
    
    data_db = dict()
    data_db['x']=[]
    data_db['y1']=[]
    data_db['y2']=[]

    for row in res:
        data_db['x'].append(row[0])
        data_db['y1'].append(row[1])
        data_db['y2'].append(row[2])

    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=data_db),200
    
@app.route('/mockup_2_4', methods = ['POST'])
def get_data2_4():

    #mockup_1_2 doesnt have any parameters
    ##Send SQL query - TODO
    #data = request.get_json()
    # ##Query
    res = cursor.execute(q.mockup_2_4)
    
    data_db = dict()
    data_db['x']=[]
    data_db['y1']=[]

    for row in res:
        data_db['x'].append(row[0])
        data_db['y1'].append(row[1])

    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=data_db),200
    
    
@app.route('/mockup_3_1', methods = ['POST'])
def get_data3_1():

    #mockup_1_2 doesnt have any parameters
    ##Send SQL query - TODO
    data = request.get_json()
    # ##Query
    year_dict = {"Y":1, "2Y":2, "3Y":3, "5Y":5}
    res = cursor.execute(q.mockup_3_1.format(data["top_n_countries"],  year_dict[data["agg"]],  data['from'], data['to']))
    
    data_db = dict()
    data_db['x']=[]
    data_db['y1']=[]
    data_db['y2']=[]

    for row in res:
        data_db['x'].append(row[0])
        data_db['y1'].append(row[1])
        data_db['y2'].append(row[2])

    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=data_db),200
    
    
@app.route('/mockup_3_2', methods = ['POST'])
def get_data3_2():

    #mockup_1_2 doesnt have any parameters
    ##Send SQL query - TODO
    data = request.get_json()
    # ##Query
    res = cursor.execute(q.mockup_3_2.format(data["country"],  data['from'], data['to']))
    
    data_db = dict()
    data_db['x']=[]
    data_db['y1']=[]
    data_db['y2']=[]

    for row in res:
        data_db['x'].append(row[0])
        data_db['y1'].append(row[1])
        data_db['y2'].append(row[2])

    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=data_db),200
    
@app.route('/mockup_4_1', methods = ['POST'])
def get_data4_1():

    #mockup_1_2 doesnt have any parameters
    ##Send SQL query - TODO
    data = request.get_json()
    # ##Query
    res = cursor.execute(q.mockup_4_1.format(data["top_n_countries"],  data['from'], data['to']))
    
    data_db = dict()
    data_db['x']=[]
    data_db['y1']=[]
    data_db['y2']=[]

    for row in res:
        data_db['x'].append(row[0])
        data_db['y1'].append(row[1])
        data_db['y2'].append(row[2])

    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=data_db),200
    
@app.route('/mockup_4_2', methods = ['POST'])
def get_data4_2():

    #mockup_1_2 doesnt have any parameters
    ##Send SQL query - TODO
    data = request.get_json()
    # ##Query
    res = cursor.execute(q.mockup_4_2.format(data["top_n_countries"],  data['from'], data['to']))
    
    data_db = dict()
    data_db['x']=[]
    data_db['y1']=[]
    data_db['y2']=[]

    for row in res:
        data_db['x'].append(row[0])
        data_db['y1'].append(row[1])
        data_db['y2'].append(row[2])

    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=data_db),200
    
@app.route('/mockup_5', methods = ['POST'])
def get_data5():

    #mockup_1_2 doesnt have any parameters
    ##Send SQL query - TODO
    data = request.get_json()
    # ##Query
    res = cursor.execute(q.mockup_5.format(data["country"],  data['from'], data['to']))
    
    data_db = dict()
    data_db['x']=[]
    data_db['y1']=[]
    data_db['y2']=[]

    for row in res:
        data_db['x'].append(row[0])
        data_db['y1'].append(row[1])
        data_db['y2'].append(row[2])

    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=data_db),200
    

    

    
    

    
    
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

users = dict()
users["admin@admin.com"]={"name": "admin", "password": "admin"}

@app.route('/login', methods=['POST'])
def get_token():
    print("login user request received !")
    credentials = request.get_json()
    print(credentials)
    print(q.login.format(credentials["username"], credentials["password"]))
    res = cursor.execute(q.login.format(credentials["username"], credentials["password"]))
    if list(res)[0][0] == 1:
        print("user authenticated !")
        return jsonify(
            isError=False,
            message="Success",
            statusCode=200,
            data={"token": "12346"}),200
    else:
        return jsonify(
            isError=False,
            message="Unauthenticated",
            statusCode=200,
            data={"token": "unAuth"}),200

@app.route('/register', methods=['POST'])
def register():
    print("new registration received !")
    data = request.get_json()
    users[data["username"]]={"name": data["name"], "password":data["password"]}
    return jsonify(
        isError=False,
        message="Success",
        statusCode=200),200

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
    if not data_db['x'] or not data_db['y1'] or not data_db['y2']:
        data_db={}
    if not data_db['x'] or not data_db['y1'] or not data_db['y2']:
        data_db={}
    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=data_db),200
    
    
@app.route('/mockup_1_2', methods = ['POST'])
def get_data1_2():

    #mockup_1_2 doesnt have any parameters
    ##Send SQL query - TODO
    data = request.get_json()
    # ##Query
    res = cursor.execute(q.mockup_1_2.format(data['from'], data['to']))
    
    data_db = dict()
    data_db['x']=[]
    data_db['y1']=[]
    for row in res:
        data_db['x'].append(row[0])
        data_db['y1'].append(row[1])

    ##Parse SQL query and Send JSON object back with x and y data for graph - TODO
    if not data_db['x'] or not data_db['y1']:
        data_db={}
    if not data_db['x'] or not data_db['y1']:
        data_db={}
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
    if not data_db['x'] or not data_db['y1'] or not data_db['y2'] or not data_db['y2'] or not data_db['y3'] or not data_db['y4']:
        data_db={}
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
    print(data)
    res = cursor.execute(q.mockup_2_1.format(data["topN"],  data['from'], data['to']))
    
    data_db = dict()
    data_db['x']=[]
    data_db['y1']=[]
    data_db['y2']=[]
    
    for row in res:
        data_db['x'].append(row[0])
        data_db['y1'].append(row[1])
        data_db['y2'].append(row[2])

    ##Parse SQL query and Send JSON object back with x and y data for graph - 
    res_data = dict()
    countries = set(data_db['y1'])
    for c in countries:
        if c not in data:
            res_data[c] = dict()
            res_data[c]['x'] = []
            res_data[c]['y'] = []

    for i,k in enumerate(data_db['y1']):
        res_data[k]['x'].append(data_db['x'][i])
        res_data[k]['y'].append(data_db['y2'][i])
    
    #print(res_data)
    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=res_data),200
    
    
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
    if not data_db['x'] or not data_db['y1'] or not data_db['y2'] or not data_db['y3']:
        data_db={}
    if not data_db['x'] or not data_db['y1'] or not data_db['y2'] or not data_db['y3']:
        data_db={}
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

    if not data_db['x'] or not data_db['y1'] or not data_db['y2']:
        data_db={}
    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=data_db),200
    
@app.route('/mockup_2_4', methods = ['POST'])
def get_data2_4():

    #mockup_1_2 doesnt have any parameters
    ##Send SQL query - TODO
    data = request.get_json()
    # ##Query
    res = cursor.execute(q.mockup_2_4.format(  data['from'], data['to']))
    
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
    res = cursor.execute(q.mockup_3_1.format(data["topN"],  year_dict[data["agg"]],  data['from'], data['to']))
    
    data_db = dict()
    data_db['x']=[]
    data_db['y1']=[]
    data_db['y2']=[]

    for row in res:
        data_db['x'].append(row[0])
        data_db['y1'].append(row[1])
        data_db['y2'].append(row[2])
        
    res_data = dict()
    countries = set(data_db['y1'])
    for c in countries:
        if c not in data:
            res_data[c] = dict()
            res_data[c]['x'] = []
            res_data[c]['y'] = []

    for i,k in enumerate(data_db['y1']):
        res_data[k]['x'].append(data_db['x'][i])
        res_data[k]['y'].append(data_db['y2'][i])

    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=res_data),200
    
    
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

    if not data_db['x'] or not data_db['y1'] or not data_db['y2']:
        data_db={}

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
    res = cursor.execute(q.mockup_4_1.format(data["topN"],  data['from'], data['to']))
    
    data_db = dict()
    data_db['x']=[]
    data_db['y1']=[]
    data_db['y2']=[]

    for row in res:
        data_db['x'].append(row[0])
        data_db['y1'].append(row[1])
        data_db['y2'].append(row[2])
    
    res_data = dict()

    minYear = min(data_db['x'])
    maxYear = max(data_db['x'])

    countries = set(data_db['y1'])
    checks = dict()
    for c in countries:
        checks[c]=dict()
        checks[c]["years"]= [None for x in range(minYear, maxYear+1)]
        checks[c]["ranks"]= [None for x in range(minYear, maxYear+1)]

    for i in range(len(data_db['x'])):
        if data_db['y1'][i] not in res_data:
            res_data[data_db['y1'][i]]=dict()

        checks[data_db['y1'][i]]["years"][data_db['x'][i]-minYear]=data_db['x'][i]
        checks[data_db['y1'][i]]["ranks"][data_db['x'][i]-minYear]=data_db['y2'][i]
        res_data[data_db['y1'][i]]['x']=checks[data_db['y1'][i]]["years"]
        res_data[data_db['y1'][i]]['y']=checks[data_db['y1'][i]]["ranks"]

    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data={"rank":res_data, "x":[i for i in range(minYear, maxYear+1)]}),200
    
@app.route('/mockup_4_2', methods = ['POST'])
def get_data4_2():

    #mockup_1_2 doesnt have any parameters
    ##Send SQL query - TODO
    data = request.get_json()
    # ##Query
    res = cursor.execute(q.mockup_4_2.format(data["topN"],  data['from'], data['to']))
    
    data_db = dict()
    data_db['x']=[]
    data_db['y1']=[]
    data_db['y2']=[]

    for row in res:
        data_db['x'].append(row[0])
        data_db['y1'].append(row[1])
        data_db['y2'].append(row[2])
        
    res_data = dict()
    countries = set(data_db['y1'])
    for c in countries:
        if c not in data:
            res_data[c] = dict()
            res_data[c]['x'] = []
            res_data[c]['y'] = []

    for i,k in enumerate(data_db['y1']):
        res_data[k]['x'].append(data_db['x'][i])
        res_data[k]['y'].append(data_db['y2'][i])

    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=res_data),200
    
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
    
@app.route('/records_count', methods = ['POST'])
def get_data_record():

    #mockup_1_2 doesnt have any parameters
    ##Send SQL query - TODO
    data = request.get_json()
    # ##Query
    res = cursor.execute(q.records_count)
    
    data_db = dict()
 
    for row in res:
        data_db['records_count'] = row[0]
    return jsonify(
        isError=False,
        message="Success",
        statusCode=200,
        data=data_db),200
    
if __name__ == '__main__':
    app.run(debug=True)  
    

    

    
    

    
    
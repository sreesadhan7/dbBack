from flask import Flask
from flask import request, jsonify
import oracledb

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
    res = cursor.execute("""
WITH gloabl_atmosphere_temp_yearly AS
    (SELECT country,
        EXTRACT(YEAR FROM time_stamp) as time_stamp,
        ROUND(AVG(temperature_monthly_mean), 2) atm_temp_yearly_mean
    FROM 
        Global_Atmosphere_Temperature 
    GROUP BY 
        country, EXTRACT(YEAR FROM time_stamp)
    ),

surface_and_atmosphere as 
    (SELECT 
        ga.country, 
        EXTRACT(YEAR FROM gs.time_stamp) year,
        atm_temp_yearly_mean atmosphere_temp, 
        temperature surface_temp
    FROM 
        gloabl_atmosphere_temp_yearly ga 
        INNER JOIN 
        Global_Surface_Temperature gs 
        ON ga.country = gs.country AND ga.time_stamp = EXTRACT(YEAR FROM gs.time_stamp)),

year_temps as 
    (SELECT * FROM surface_and_atmosphere WHERE 
        country = 'Afghanistan' ORDER BY year
    ),

year_temp_country_code AS
    (
        SELECT 
            cp.c_code_ISO3 country, 
            year, 
            atmosphere_temp, 
            surface_temp 
        FROM 
            year_temps yt 
            INNER JOIN country_prime cp ON yt.country = cp.country_source
    ),

YearGroups AS (
    SELECT 
        year,
        country,
        surface_temp,
        atmosphere_temp,
        ceil(((year - MIN(year-1) OVER ())/5)) AS year_group
    FROM 
        year_temp_country_code ORDER BY year
)
--SELECT * FROM YearGroups;
SELECT 
    MIN (year) YEAR,
    avg(surface_temp) avg_surface_temp,
    avg(atmosphere_temp) avg_atmosphere_Temp
FROM 
    YearGroups
WHERE
    year > 1960 and year <= 2022
GROUP BY
    year_group
ORDER BY
    YEAR""")
    
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
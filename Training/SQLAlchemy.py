from sqlalchemy import create_engine
import pandas as pd
from flask import jsonify, Flask, request

SERVER = 'GAREEBOOO'
DATABASE = 'IndustrialWatch'
DRIVER = 'SQL Server Native Client 11.0'
USERNAME = 'sa'
PASSWORD = 'usama123'
DATABASE_CONNECTION = f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'

app = Flask(__name__)

@app.route('/getAllEmployees')
def getAllEmployees():
    engine = create_engine(DATABASE_CONNECTION)
    connection = engine.connect()

    sql = "SELECT * FROM EMPLOYEE"
    df = pd.read_sql_query(sql, connection)
    json_data = df.to_json(orient='records')

    return jsonify(json_data)


@app.route('/getEmployee/<string:name>')
def getEmployee(name):
    engine = create_engine(DATABASE_CONNECTION)
    connection = engine.connect()

    sql = f"SELECT * FROM EMPLOYEE WHERE name = '{name}'"
    df = pd.read_sql_query(sql, connection)
    json_data = df.to_json(orient='records')

    return jsonify(json_data)

@app.route('/addEmployee',  methods=['POST'])
def addEmployee():
    if request.method == 'POST':
        data = request.get_json()  # Assuming JSON data is sent in the request
        name = data.get('name')
        salary = data.get('salary')
        # Add more fields as needed

        # Connect to the database and insert the new employee data
        engine = create_engine(DATABASE_CONNECTION)
        connection = engine.connect()

        sql1 = "SELECT * FROM EMPLOYEE"
        df = pd.read_sql_query(sql1, connection)
        print(df)

        # Assuming EMPLOYEE table has columns 'name' and 'age'
        sql = f"INSERT INTO EMPLOYEE (name, salary) VALUES (?,?)"
        print(sql)
        connection.execute(statement=sql, parameters={'name':name,'salary':salary})

        return jsonify({"message": "Employee added successfully"})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5500)

sql = "SELECT * FROM EMPLOYEE"
df = pd.read_sql_query(sql, connection)


# Set display options to show more rows and columns
pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # Set the display width to fit content

print(df[['id','name','salary']].head(3))

result_df = df[df['id'] == 1]

print('Getting the desired Record!')
print(result_df)

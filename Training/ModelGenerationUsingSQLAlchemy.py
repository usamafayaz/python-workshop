from sqlalchemy import create_engine, MetaData
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session

SERVER = 'GAREEBOOO'
DATABASE = 'IndustrialWatch'
DRIVER = 'SQL Server Native Client 11.0'
USERNAME = 'sa'
PASSWORD = 'usama123'
DATABASE_CONNECTION = f'mssql://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver={DRIVER}'

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_CONNECTION)
# connection = engine.connect()

# Reflect the database
metaData = MetaData()
metaData.reflect(bind=engine)

# Use automap to create mapped classes
Base = automap_base(metadata=metaData)
Base.prepare()

 # Access the mapped classes
Employee = Base.classes.Employee  # Replace 'Employee' with the actual table name

# Create a session
session = Session(engine)

# Example: Query all employees and print their information
employees = session.query(Employee).all()
for employee in employees:
    print(f"ID: {employee.id}, Name: {employee.name}, Salary: {employee.salary}, Gender: {employee.gender}")


# sql = "SELECT * FROM EMPLOYEE"
# df = pd.read_sql_query(sql, connection)
# print(df)


import urllib
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

driver = os.getenv('AZURE_SQL_DRIVER')
server = os.getenv('AZURE_SQL_SERVER')
port = os.getenv("AZURE_SQL_PORT")
database = os.getenv('AZURE_SQL_DATABASE')
username = os.getenv('AZURE_SQL_USER')
password = os.getenv('AZURE_SQL_PASSWORD')


odbc_str = f"DRIVER={driver};SERVER={server};PORT={port};UID={username};DATABASE={database};PWD={password}"
connect_str = 'mssql+pyodbc:///?odbc_connect=' + urllib.parse.quote_plus(odbc_str)

engine = create_engine(connect_str)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

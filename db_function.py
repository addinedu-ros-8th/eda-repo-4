import database_connect
import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PORT = os.getenv("DB_PORT")

def get_db(DB_HOST=DB_HOST, DB_USER=DB_USER, DB_PASSWORD=DB_PASSWORD, DB_PORT=DB_PORT, DB_NAME=DB_NAME):
    db = database_connect.DB(DB_HOST, DB_USER, DB_PASSWORD, DB_PORT, DB_NAME)
    db.connect()
    return db

def get_db_engine(DB_USER=DB_USER, DB_PASSWORD=DB_PASSWORD, DB_HOST=DB_HOST, DB_NAME=DB_NAME):
    return create_engine(f'mysql+mysqldb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

def create_table_from_df(df, table_name, engine):
    metadata = MetaData()
    columns = []
    
    for col, dtype in zip(df.columns, df.dtypes):
        if dtype == 'int64':
            columns.append(Column(col, Integer))
        elif dtype == 'float64':
            columns.append(Column(col, Float))
        elif dtype == 'object':
            columns.append(Column(col, String(10)))

    Table(table_name, metadata, *columns)
    metadata.create_all(engine)

    print(f"Table {table_name} created")

def insert_table_from_df(df, table_name, engine):
    with engine.connect() as conn:
        df.to_sql(table_name, conn, if_exists='append', index=False)

    print(f"Inserted {len(df)} rows into {table_name}")

def initialize_table_from_df(df, table_name, engine):
    try:
        create_table_from_df(df, table_name, engine)
    except:
        print(f"Table {table_name} already exists")
    insert_table_from_df(df, table_name, engine)

def get_table_from_db(table_name, engine):
    return pd.read_sql(f"SELECT * FROM {table_name}", engine)

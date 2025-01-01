import database_connect
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PORT = os.getenv("DB_PORT")

def get_db():
    db = database_connect.DB(DB_HOST, DB_USER, DB_PASSWORD, DB_PORT, DB_NAME)
    db.connect()
    return db


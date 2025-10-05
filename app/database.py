import psycopg2
import os
from . import config

DB_PASSWORD = os.getenv("DB_PASSWORD")

DATABASE_URL = f"dbname=operator_db user=postgres password={DB_PASSWORD}"

def get_db_connection():

    conn = psycopg2.connect(DATABASE_URL,host="db")
    return conn
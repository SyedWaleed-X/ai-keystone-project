import psycopg2
import os
from . import config

DATABASE_URL = f"dbname=operator_db user=postgres password={config.DB_PASSWORD}"

def get_db_connection():

    conn = psycopg2.connect(DATABASE_URL)
    return conn
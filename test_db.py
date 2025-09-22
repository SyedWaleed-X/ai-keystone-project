# test_db.py
import psycopg2

# Make sure this connection string is IDENTICAL to the one in your database.py
DATABASE_URL = "dbname=operator_db user=postgres password=gintokipr02312"

print("Attempting to connect to the database...")

try:
    # Add a special 'host' parameter to be explicit
    conn = psycopg2.connect(DATABASE_URL, host="localhost")
    print("✅ Connection successful!")
    
    # Let's try to fetch something simple
    cur = conn.cursor()
    cur.execute("SELECT version();") # A simple query to get the PostgreSQL version
    db_version = cur.fetchone()
    print(f"✅ PostgreSQL Version: {db_version[0]}")
    
    cur.close()
    conn.close()
    print("✅ Connection closed.")

except Exception as e:
    print("\n❌ CONNECTION FAILED. Here is the error:")
    print(e)
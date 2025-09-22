# app/main.py

from fastapi import FastAPI
import psycopg2
import psycopg2.extras
from app import database, schemas

# This is the one and only 'app' instance
app = FastAPI()

# This is our root endpoint
@app.get("/")
def read_root():
    return {"message": "Operator API is online."}

# This is the one and only '/employees' endpoint
# This is the "Fake Data" test version for app/main.py

# The final, permanent, robust version for app/main.py

@app.get("/employees", response_model=list[schemas.Employee])
def get_all_employees():
    conn = None
    try:
        conn = database.get_db_connection()
        cur = conn.cursor() # Use a standard cursor, not a DictCursor
        
        cur.execute("SELECT id, name, hire_date, salary, department_id FROM employees;")
        
        # Get the column names from the cursor description
        colnames = [desc[0] for desc in cur.description]
        
        # Fetch all rows
        rows = cur.fetchall()
        
        # Manually build a list of dictionaries
        employees = []
        for row in rows:
            employees.append(dict(zip(colnames, row)))
            
        cur.close()
        return employees
        
    finally:
        if conn:
            conn.close()

@app.get("/departments", response_model=list[schemas.departments])

def get_all_departments():
    conn = None
    try:
        conn = database.get_db_connection()
        cur = conn.cursor() # Use a standard cursor, not a DictCursor
        cur.execute("SELECT id, department_name FROM departments;")

        # Get the column names from the cursor description
        colnames = [desc[0] for desc in cur.description]
        rows = cur.fetchall()
        departments = []

        for row in rows:
            departments.append(dict(zip(colnames, row)))
        cur.close()
        return departments
    finally:
        if conn:
            conn.close()

# app/main.py

from fastapi import FastAPI
import psycopg2
import psycopg2.extras
from app import database, schemas
from psycopg2.extras import DictCursor
# This is the one and only 'app' instance
from fastapi import HTTPException
from typing import Optional
from app.rag_prototype import RAG_Pipeline
from contextlib import asynccontextmanager

ml_models = {}

@asynccontextmanager

async def lifespan(app:FastAPI):

    ml_models["rag_pipeline"] = RAG_Pipeline()

    yield

    print("Server shutting down")

    ml_models.clear()


app = FastAPI(lifespan=lifespan)

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



@app.get("/employees/{employee_id}", response_model=schemas.Employee)
def get_employee_by_id(employee_id: int):
    conn = None
    try:
        conn = database.get_db_connection()
        cur = conn.cursor()
        
        # 1. Define the SQL and params separately for security
        sql = "SELECT * FROM employees WHERE id = %s"
        params = (employee_id,)
        
        # 2. Execute safely
        cur.execute(sql, params)
        
        # 3. Fetch ONLY ONE record, since we are searching by a unique ID
        row = cur.fetchone()
        
        # 4. CRITICAL: Handle the case where no employee was found
        if row is None:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        # 5. Build the dictionary for the single employee found
        colnames = [desc[0] for desc in cur.description]
        employee = dict(zip(colnames, row))
            
        cur.close()
        
        # 6. Return the single dictionary, not a list
        return employee
        
    finally:
        if conn:
            conn.close()


@app.get("/search/employees", response_model=list[schemas.Employee])

def search_employee(department: Optional[str] = None, min_salary: int | None = None ):
    conn = None
    try:
        conn = database.get_db_connection()
        cur = conn.cursor()
        
        # 1. Define the SQL and params separately for security
        sql = "SELECT * FROM employees WHERE 1=1 "
        params = []

        if department:
            sql += "AND  department_id = (Select id from departments where department_name = %s)"
            params.append(department)
        if min_salary:
            sql += " And salary >= %s"
            params.append(min_salary)        
        # 2. Execute safely
        cur.execute(sql, tuple(params))
        
        # 3. Fetch ONLY ONE record, since we are searching by a unique ID
        rows = cur.fetchall()
        
        # 4. CRITICAL: Handle the case where no employee was found
        

        
        # 5. Build the dictionary for the single employee found
        colnames = [desc[0] for desc in cur.description]
        employees = [dict(zip(colnames, row)) for row in rows]
            
        cur.close()
        
        # 6. Return the single dictionary, not a list
        return employees
        
    finally:
        if conn:
            conn.close()

@app.post("/employees", response_model=list[schemas.Employee])

def emp_post(employee: schemas.EmployeeCreate):

    conn = None 

    try:

        conn = database.get_db_connection()

#cursor is the robot arm that goes to to the warehouse to do stuff

        cur = conn.cursor()

        sql = """
insert into employees (name,hire_date, salary,department_id) 
values (%s,%s,%s,%s)
 RETURNING *

"""
        params = (employee.name, employee.hire_date, employee.salary, employee.department_id)

        cur.execute(sql,params)

        new_emp_row = cur.fetchone()
#commit finalizes , otherwise database doesnt save info, doesnt give af, forgets.
        conn.commit()

        cur.close()

        colname = [desc[0] for desc in cur.description]
        new_emp_dict = [dict(zip(colname, new_emp_row))]

        return new_emp_dict

    finally:
        if conn:
            conn.close()







@app.post("/chat",response_model=schemas.ChatResponse)

async def chat_endpoint(query: schemas.ChatQuery):


    user_query = query.query

    if not user_query or user_query.strip() == "":

        raise HTTPException(status_code=400, detail="Query cant be empty")
    

    rag_pipe = ml_models["rag_pipeline"]

    answer = rag_pipe.ask(user_query)

    return answer






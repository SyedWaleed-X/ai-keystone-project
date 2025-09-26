


# Project title : Employee and department Data API project

A REST API built with python, postgreSQL, and FASTAPI to manage employee data and departments for a corporate environment.


# features

The api can insert employees, fetch all employees, fetch one employee, sort employees by department id and minsalary.
Data is consistent.
Documentation is provided by FASTAPI, which is quite ntuitive and easy to use and understand.

## Tech Stack

*   **Backend:** Python 3.11+, FastAPI
*   **Database:** PostgreSQL
*   **Driver:** Psycopg2
*   **Server:** Uvicorn

---



## Local Setup

To run this project on your local machine, please follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/SyedWaleed-X/ai-keystone-project.git
    cd ai-keystone-project
    ```

2.  **Create and Activate Virtual Environment:**
    ```bash
    # For Windows
    python -m venv .venv
    .\.venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Database Setup:**
    *   Ensure you have PostgreSQL installed and running.
    *   Create a new database named `operator_db`.
    *   Execute the SQL scripts in the `/sql` folder in the following order:
        1.  `schema.sql` (to create the tables)
        2.  `seeds.sql` (to populate with sample data)

5.  **Configure Environment:**
    *   Create a `config.py` file in the root directory.
    *   Add your database password to this file: `DB_PASSWORD = "your_password"`

6.  **Run the Server:**
    ```bash
    uvicorn app.main:app --reload
    ```

7.  **Access the API:**
    *   The API will be available at `http://127.0.0.1:8000`.
    *   Interactive documentation is available at `http://127.0.0.1:8000/docs`.

---

## API Endpoints

### Employees

*   **GET `/employees`**: Fetches a list of all employees.
    *   **Response:** `200 OK`
      ```json
      [
        {
          "id": 1,
          "name": "John Smith",
          "hire_date": "2024-03-15",
          "salary": 70000,
          "department_id": 1
        }
      ]
      ```

*   **GET `/employees/{employee_id}`**: Fetches a single employee by their ID.
    *   **Response:** `200 OK` or `404 Not Found`

*   **GET `/search/employees`**: Searches for employees.
    *   **Query Parameter:** `department` (e.g., `/search/employees?department=Sales`)
    *   **Response:** `200 OK`







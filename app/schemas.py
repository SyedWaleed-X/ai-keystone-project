# app/schemas.py
from pydantic import BaseModel
from datetime import date
from typing import Optional

class Employee(BaseModel):
    id: int
    name: str
    hire_date: Optional[date] = None
    salary: Optional[int] = None
    department_id: Optional[int] = None

class departments(BaseModel):
    id: int
    department_name: str
# app/schemas.py
from pydantic import BaseModel
from datetime import date
from typing import Optional, List, Dict, Any

class Employee(BaseModel):
    id: int
    name: str
    hire_date: Optional[date] = None
    salary: Optional[int] = None
    department_id: Optional[int] = None

class departments(BaseModel):
    id: int
    department_name: str

class EmployeeCreate(BaseModel):
    name: str
    hire_date: Optional[date] = None
    salary: Optional[int] = None
    department_id: Optional[int] = None

class ChatQuery(BaseModel):
    query:str

class ChatResponse(BaseModel):
    answer:str
    source_documents: Optional[List[str]] = None
    source_metadatas: Optional[List[Dict[str, Any]]] = None
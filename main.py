from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Doorline Rotation Manager")

employees = []

class Employee(BaseModel):
    firstname: str
    lastname: str
    status: str = "Verfügbar"

@app.get("/")
def home():
    return {
        "app": "Doorline Rotation Manager",
        "status": "running"
    }

@app.get("/employees")
def get_employees():
    return employees

@app.post("/employees")
def add_employee(employee: Employee):
    employees.append(employee.model_dump())
    return employee

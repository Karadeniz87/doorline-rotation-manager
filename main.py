from fastapi import FastAPI
from employee import Employee

app = FastAPI(title="Doorline Rotation Manager")

employees = []


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


@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee):
    if employee_id >= len(employees):
        return {"message": "Mitarbeiter nicht gefunden"}

    employees[employee_id] = employee.model_dump()
    return employees[employee_id]


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    if employee_id >= len(employees):
        return {"message": "Mitarbeiter nicht gefunden"}

    deleted_employee = employees.pop(employee_id)

    return {
        "message": "Mitarbeiter gelöscht",
        "employee": deleted_employee
    }    return {
        "message": "Mitarbeiter nicht gefunden"
    }
@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee):
    if employee_id >= len(employees):
        return {"message": "Mitarbeiter nicht gefunden"}

    employees[employee_id] = employee.model_dump()
    return employees[employee_id]


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    if employee_id >= len(employees):
        return {"message": "Mitarbeiter nicht gefunden"}

    deleted_employee = employees.pop(employee_id)

    return {
        "message": "Mitarbeiter gelöscht",
        "employee": deleted_employee
    }

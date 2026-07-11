from fastapi import FastAPI, HTTPException
from employee import Employee

app = FastAPI(
    title="Doorline Rotation Manager",
    version="1.0.0"
)

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


@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    if employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    return employees[employee_id]


@app.post("/employees")
def add_employee(employee: Employee):
    employee_data = employee.model_dump()

    employees.append(employee_data)

    return {
        "message": "Mitarbeiter hinzugefügt",
        "employee_id": len(employees) - 1,
        "employee": employee_data
    }


@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee):
    if employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    employees[employee_id] = employee.model_dump()

    return {
        "message": "Mitarbeiter aktualisiert",
        "employee": employees[employee_id]
    }


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    if employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    deleted_employee = employees.pop(employee_id)

    return {
        "message": "Mitarbeiter gelöscht",
        "employee": deleted_employee
    }def add_employee(employee: Employee):
    employee_data = employee.model_dump()

    employees.append(employee_data)

    return {
        "message": "Mitarbeiter hinzugefügt",
        "employee_id": len(employees) - 1,
        "employee": employee_data
    }


@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee):
    if employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    employees[employee_id] = employee.model_dump()

    return {
        "message": "Mitarbeiter aktualisiert",
        "employee": employees[employee_id]
    }


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    if employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    deleted_employee = employees.pop(employee_id)

    return {
        "message": "Mitarbeiter gelöscht",
        "employee": deleted_employee
    }@app.post("/employees")
def add_employee(employee: Employee):
    employee_data = employee.model_dump()

    employees.append(employee_data)

    return {
        "message": "Mitarbeiter hinzugefügt",
        "employee_id": len(employees) - 1,
        "employee": employee_data
    }


@app.put("/employees/{employee_id}")
def update_employee(employee_id: int, employee: Employee):

    if employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    employees[employee_id] = employee.model_dump()

    return {
        "message": "Mitarbeiter aktualisiert",
        "employee": employees[employee_id]
    }


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):

    if employee_id >= len(employees):
        raise HTTPException(
            status_code=404,
            detail="Mitarbeiter nicht gefunden"
        )

    deleted_employee = employees.pop(employee_id)

    return {
        "message": "Mitarbeiter gelöscht",
        "employee": deleted_employee
    }@app.delete("/employees/{employee_id}")
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

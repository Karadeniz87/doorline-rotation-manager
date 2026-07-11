employees = []

def add_employee(firstname, lastname):
    employees.append({
        "firstname": firstname,
        "lastname": lastname,
        "status": "Verfügbar"
    })

def get_employees():
    return employees

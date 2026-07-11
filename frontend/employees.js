const API_URL =
    "https://doorline-rotation-manager.onrender.com";

async function loadEmployees() {

    const response =
        await fetch(
            `${API_URL}/employees`
        );

    const employees =
        await response.json();

    const container =
        document.getElementById(
            "employees_container"
        );

    container.innerHTML = "";

    employees.forEach(
        (employee, index) => {

        container.innerHTML += `
            <div class="card">

                <h2>
                    ${employee.firstname}
                    ${employee.lastname}
                </h2>

                <p>
                    📍 Station:
                    ${
                        employee.station ||
                        "Support"
                    }
                </p>

                <p>
                    ⚖️ Fairness:
                    ${
                        employee.fairness_points
                    }
                </p>

                <label class="skill-item">
                    <input
                        type="checkbox"
                        ${
                            employee.is_sick
                            ? "checked"
                            : ""
                        }
                        onchange="
                            updateEmployee(
                                ${index},
                                'is_sick',
                                this.checked
                            )
                        "
                    >
                    🤒 Krank
                </label>

                <label class="skill-item">
                    <input
                        type="checkbox"
                        ${
                            employee.is_vacation
                            ? "checked"
                            : ""
                        }
                        onchange="
                            updateEmployee(
                                ${index},
                                'is_vacation',
                                this.checked
                            )
                        "
                    >
                    🏖 Urlaub
                </label>

            </div>
        `;
    });
}

async function updateEmployee(
    employeeId,
    field,
    value
) {

    const response =
        await fetch(
            `${API_URL}/employees/${employeeId}`
        );

    const employee =
        await response.json();

    employee[field] = value;

    await fetch(
        `${API_URL}/employees/${employeeId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify(
                employee
            )
        }
    );

    loadEmployees();
}

loadEmployees();

const API =
    "https://doorline-rotation-manager.onrender.com";


async function loadEmployees() {

    const response =
        await fetch(`${API}/employees`);

    const employees =
        await response.json();

    const container =
        document.getElementById(
            "employee_list"
        );

    container.innerHTML = "";

    employees.forEach((employee, index) => {

        container.innerHTML += `
            <div class="card">

                <h3>
                    ${employee.firstname}
                    ${employee.lastname}
                </h3>

                <p>
                    Status:
                    ${employee.status}
                </p>

                <p>
                    Fairness:
                    ${employee.fairness_points || 0}
                </p>

                <button
                    onclick="deleteEmployee(${index})">

                    🗑 Löschen

                </button>

            </div>
        `;
    });
}


async function addEmployee() {

    const firstname =
        document.getElementById(
            "firstname"
        ).value;

    const lastname =
        document.getElementById(
            "lastname"
        ).value;

    const status =
        document.getElementById(
            "status"
        ).value;

    await fetch(
        `${API}/employees`,
        {
            method: "POST",

            headers: {
                "Content-Type":
                    "application/json"
            },

            body: JSON.stringify({
                firstname,
                lastname,
                status,
                fairness_points: 0
            })
        }
    );

    loadEmployees();
}


async function deleteEmployee(id) {

    await fetch(
        `${API}/employees/${id}`,
        {
            method: "DELETE"
        }
    );

    loadEmployees();
}

loadEmployees();

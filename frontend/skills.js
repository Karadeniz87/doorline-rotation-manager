const STATIONS = [
    "30L", "30R",
    "40L", "40R",
    "50L", "50R",
    "60L", "60R",
    "70L", "70R",
    "80L", "80R",
    "90L", "90R",
    "100L", "100R",
    "110L", "110R"
];

async function loadSkills() {

    const response = await fetch("/employees");
    const employees = await response.json();

    const container =
        document.getElementById(
            "skills_container"
        );

    container.innerHTML = "";

    employees.forEach((employee, index) => {

        let html = `
            <div class="card">

                <h2>
                    ${employee.firstname}
                    ${employee.lastname}
                </h2>

                <div class="skills-grid">
        `;

        STATIONS.forEach(station => {

            const checked =
                employee[`skill_${station}`]
                    ? "checked"
                    : "";

            html += `
                <label class="skill-item">
                    <input
                        type="checkbox"
                        ${checked}
                        onchange="
                            updateEmployee(
                                ${index},
                                'skill_${station}',
                                this.checked
                            )
                        "
                    >
                    ${station}
                </label>
            `;
        });

        html += `
                </div>

                <hr>

                <label class="skill-item">
                    <input
                        type="checkbox"
                        ${employee.is_sick ? "checked" : ""}
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
                        ${employee.is_vacation ? "checked" : ""}
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

                <p>
                    📍 Aktuelle Station:
                    ${employee.station || "-"}
                </p>

                <p>
                    🔄 Letzte Station:
                    ${employee.last_station || "-"}
                </p>

                <p>
                    ⚖️ Fairness:
                    ${employee.fairness_points}
                </p>

            </div>
        `;

        container.innerHTML += html;
    });
}

async function updateEmployee(
    employeeId,
    field,
    value
) {

    const response =
        await fetch(
            `/employees/${employeeId}`
        );

    const employee =
        await response.json();

    employee[field] = value;

    await fetch(
        `/employees/${employeeId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify(employee)
        }
    );

    loadSkills();
}

loadSkills();

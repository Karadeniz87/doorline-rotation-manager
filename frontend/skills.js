const API = "https://doorline-rotation-manager.onrender.com";

const stations = [
    "30L","30R",
    "40L","40R",
    "50L","50R",
    "60L","60R",
    "70L","70R",
    "80L","80R",
    "90L","90R",
    "100L","100R",
    "110L","110R"
];

async function loadSkills() {

    const response = await fetch(`${API}/employees`);
    const employees = await response.json();

    const container =
        document.getElementById("employeeSkills");

    container.innerHTML = "";

    employees.forEach((employee, index) => {

        let html = `
        <div class="section">
            <h3>
                ${employee.firstname}
                ${employee.lastname}
            </h3>
        `;

        stations.forEach(station => {

            const checked =
                employee[`skill_${station}`]
                    ? "checked"
                    : "";

            html += `
                <label>
                    <input
                        type="checkbox"
                        ${checked}
                        onchange="
                            updateSkill(
                                ${index},
                                '${station}',
                                this.checked
                            )
                        "
                    >
                    ${station}
                </label>
                <br>
            `;
        });

        html += `</div>`;

        container.innerHTML += html;
    });
}

async function updateSkill(
    employeeId,
    station,
    value
) {

    const response =
        await fetch(
            `${API}/employees/${employeeId}`
        );

    const employee =
        await response.json();

    employee[`skill_${station}`] = value;

    await fetch(
        `${API}/employees/${employeeId}`,
        {
            method: "PUT",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify(employee)
        }
    );
}

loadSkills();

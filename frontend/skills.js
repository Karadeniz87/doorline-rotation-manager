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

    try {

        const response = await fetch("/employees");
        const employees = await response.json();

        const container =
            document.getElementById(
                "skills_container"
            );

        container.innerHTML = "";

        employees.forEach(employee => {

            let skillsHtml = "";

            stations.forEach(station => {

                const skillName =
                    `skill_${station}`;

                skillsHtml += `
                    <label class="skill-item">

                        <input
                            type="checkbox"
                            ${employee[skillName] ? "checked" : ""}
                            onchange="
                                updateSkill(
                                    ${employee.id},
                                    '${skillName}',
                                    this.checked
                                )
                            "
                        >

                        ${station}

                    </label>
                `;
            });

            container.innerHTML += `
                <div class="employee-card">

                    <h3>
                        ${employee.firstname}
                        ${employee.lastname}
                    </h3>

                    <div class="skills-grid">
                        ${skillsHtml}
                    </div>

                </div>
            `;
        });

    } catch (error) {

        console.error(
            "Fehler beim Laden:",
            error
        );
    }
}

async function updateSkill(
    employeeId,
    skillName,
    value
) {

    try {

        const employeeResponse =
            await fetch(
                `/employees/${employeeId}`
            );

        const employee =
            await employeeResponse.json();

        employee[skillName] = value;

        const saveResponse =
            await fetch(
                `/employees/${employeeId}`,
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

        if (!saveResponse.ok) {
            throw new Error(
                "Speichern fehlgeschlagen"
            );
        }

        console.log(
            `${skillName} gespeichert`
        );

    } catch (error) {

        console.error(
            "Speicherfehler:",
            error
        );

        alert(
            "Skill konnte nicht gespeichert werden."
        );
    }
}

window.onload = function () {
    loadSkills();
};

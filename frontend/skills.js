const API_URL =
    "https://doorline-rotation-manager.onrender.com";

const STATIONS = [
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

        const response =
            await fetch(
                `${API_URL}/employees`
            );

        const employees =
            await response.json();

        const container =
            document.getElementById(
                "skills_container"
            );

        container.innerHTML = "";

        employees.forEach(
            (employee, index) => {

            let html = `
                <div class="card">
                    <h2>
                        ${employee.firstname}
                        ${employee.lastname}
                    </h2>

                    <div class="skills-grid">
            `;

            STATIONS.forEach(
                station => {

                const checked =
                    employee[
                        `skill_${station}`
                    ]
                        ? "checked"
                        : "";

                html += `
                    <label class="skill-item">
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
                `;
            });

            html += `
                    </div>
                </div>
            `;

            container.innerHTML += html;
        });

    } catch(error) {

        console.error(
            error
        );
    }
}

async function updateSkill(
    employeeId,
    station,
    value
) {

    try {

        const response =
            await fetch(
                `${API_URL}/employees/${employeeId}`
            );

        const employee =
            await response.json();

        employee[
            `skill_${station}`
        ] = value;

        const saveResponse =
            await fetch(
                `${API_URL}/employees/${employeeId}`,
                {
                    method:"PUT",
                    headers:{
                        "Content-Type":
                            "application/json"
                    },
                    body:JSON.stringify(
                        employee
                    )
                }
            );

        if(
            saveResponse.ok
        ){
            console.log(
                "Skill gespeichert"
            );
        }

    } catch(error){

        console.error(
            error
        );
    }
}

loadSkills();

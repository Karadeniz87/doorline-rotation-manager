async function loadStats() {

    try {

        const response = await fetch("/stats");
        const stats = await response.json();

        document.getElementById("employees_total").innerText =
            stats.employees_total || 0;

        document.getElementById("available").innerText =
            stats.available || 0;

        document.getElementById("vacation").innerText =
            stats.vacation || 0;

        document.getElementById("sick").innerText =
            stats.sick || 0;

        document.getElementById("support").innerText =
            stats.support || 0;

        document.getElementById("double_takt").innerText =
            stats.double_takt || 0;

    } catch (error) {
        console.error(
            "Fehler beim Laden der KPIs:",
            error
        );
    }
}


async function loadStations() {

    try {

        const response =
            await fetch("/stations");

        const stations =
            await response.json();

        const container =
            document.getElementById(
                "stations_container"
            );

        if (!container) return;

        container.innerHTML = "";

        for (let i = 0; i < stations.length; i += 2) {

            const left = stations[i];

            const right = stations[i + 1] || {
                station: "",
                employee: null
            };

let statusClass = "green-status";

/* Beide Stationen leer */
if (
    !left.employee &&
    !right.employee
){
    statusClass = "red-status";
}

/* Eine Seite besetzt */
else if (
    !left.employee ||
    !right.employee
){
    statusClass = "yellow-status";
}

/* Doppeltakt Stationen */
const doubleTaktStations = [
    "40L","40R",
    "50L","50R",
    "60L","60R",
    "70L","70R"
];

if(
    doubleTaktStations.includes(
        left.station
    )
){
    statusClass = "yellow-status";
}

            container.innerHTML += `
                <div class="station-row">

                    <div class="station-left">
                        <h3>${left.station}</h3>
                        <p>
                            👤 ${left.employee || "Nicht besetzt"}
                        </p>
                    </div>

                <div class="production-line">
    <div class="
        status-circle
        ${statusClass}
    "></div>
</div>

                    <div class="station-right">
                        <h3>${right.station}</h3>
                        <p>
                            👤 ${right.employee || "Nicht besetzt"}
                        </p>
                    </div>

                </div>
            `;
        }

    } catch (error) {

        console.error(
            "Stationsfehler:",
            error
        );
    }
}


async function runRotation() {

    try {

        const response =
            await fetch(
                "/rotation/run",
                {
                    method: "POST"
                }
            );

        const data =
            await response.json();
        const statusElement =
    document.getElementById(
        "staffing_status"
    );

if (data.staffing_status === "green") {
    statusElement.innerHTML =
        "🟢 Voll besetzt";
}

else if (data.staffing_status === "yellow") {
    statusElement.innerHTML =
        "🟡 Support benötigt";
}

else {
    statusElement.innerHTML =
        "🔴 Unterbesetzt";
}

        const container =
            document.getElementById(
                "stations_container"
            );

        container.innerHTML = "";

        data.stations.forEach(station => {

    const doubleTaktStations = [
        "40L","40R",
        "50L","50R",
        "60L","60R",
        "70L","70R"
    ];

    const isDouble =
        doubleTaktStations.includes(
            station.station
        );

    container.innerHTML += `
        <div class="station-card">

            <h3>${station.station}</h3>

            <p>
                👤 ${
                    station.employee
                    ? station.employee
                    : "Nicht besetzt"
                }
            </p>

            ${
                isDouble
                ? `
                <small>
                    🔵 Doppeltakt möglich
                </small>
                `
                : ""
            }

        </div>
    `;
});

        const result =
            document.getElementById(
                "rotation_result"
            );

        if (result) {
            result.innerText =
                JSON.stringify(
                    data,
                    null,
                    2
                );
        }

        loadStats();
        loadHistory();
        loadFairness();

    } catch (error) {

        console.error(
            "Rotation Fehler:",
            error
        );

        const result =
            document.getElementById(
                "rotation_result"
            );

        if (result) {
            result.innerText =
                "Fehler bei der Rotation.";
        }
    }
}


async function loadEmployees() {

    try {

        const response =
            await fetch("/employees");

        const employees =
            await response.json();

        const container =
            document.getElementById(
                "employees_container"
            );

        if (!container) return;

        container.innerHTML = "";

        employees.forEach(employee => {

            container.innerHTML += `
                <div class="employee-card">

                    <h3>
                        ${employee.firstname}
                        ${employee.lastname}
                    </h3>

                    <p>
                        Station:
                        ${
                            employee.station
                            || "-"
                        }
                    </p>

                    <p>
                        Fairness:
                        ${employee.fairness_points}
                    </p>

                    ${
                        employee.is_sick
                        ? "<p>🤒 Krank</p>"
                        : ""
                    }

                    ${
                        employee.is_vacation
                        ? "<p>🌴 Urlaub</p>"
                        : ""
                    }

                </div>
            `;
        });

    } catch (error) {

        console.error(
            "Employee Fehler:",
            error
        );
    }
}


async function loadFairness() {

    try {

        const response =
            await fetch("/fairness");

        const fairness =
            await response.json();

        const container =
            document.getElementById(
                "fairness_container"
            );

        if (!container) return;

        container.innerHTML = "";

        Object.entries(
            fairness
        ).forEach(
            ([name, points]) => {

                container.innerHTML += `
                    <div class="fairness-item">

                        <strong>
                            ${name}
                        </strong>

                        <span>
                            ${points}
                        </span>

                    </div>
                `;
            }
        );

    } catch (error) {

        console.error(
            "Fairness Fehler:",
            error
        );
    }
}


async function loadHistory() {

    try {

        const response =
            await fetch("/history");

        const history =
            await response.json();

        const container =
            document.getElementById(
                "history_container"
            );

        if (!container) return;

        container.innerHTML = "";

        history.forEach(entry => {

            container.innerHTML += `
                <div class="history-item">

                    <strong>
                        ${entry.employee_name}
                    </strong>

                    →

                    ${entry.station}

                </div>
            `;
        });

    } catch (error) {

        console.error(
            "History Fehler:",
            error
        );
    }
}


window.onload = function () {

    loadStats();

    loadStations();

    loadEmployees();

    loadFairness();

    loadHistory();

    const role = localStorage.getItem("role");

if (role === "teamlead_sp") {

    document.querySelectorAll(".admin-only")
        .forEach(element => {
            element.style.display = "none";
        });

}

};
// ----------------------------
// Rollenprüfung TL SP
// ----------------------------

const role = localStorage.getItem("role");

if (role === "teamlead_sp") {

    const skillButton =
        document.getElementById("skill_button");

    if (skillButton) {
        skillButton.style.display = "none";
    }

}

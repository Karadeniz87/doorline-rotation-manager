async function loadStats() {

    const response = await fetch("/stats");
    const stats = await response.json();

    document.getElementById(
        "employees_total"
    ).innerText =
        stats.employees_total;

    document.getElementById(
        "available"
    ).innerText =
        stats.available;

    document.getElementById(
        "vacation"
    ).innerText =
        stats.vacation;

    document.getElementById(
        "sick"
    ).innerText =
        stats.sick;

    document.getElementById(
        "support"
    ).innerText =
        stats.support;

    document.getElementById(
        "double_takt"
    ).innerText =
        stats.double_takt;
}


async function runRotation() {

    const response =
        await fetch(
            "/rotation/run",
            {
                method: "POST"
            }
        );

    const data =
        await response.json();

    const container =
        document.getElementById(
            "stations_container"
        );

    container.innerHTML = "";

    data.stations.forEach(
        station => {

        container.innerHTML += `
            <div class="station">

                <h3>
                    ${station.name}
                </h3>

                <p>
                    ${
                        station.employee_1
                        || "Nicht besetzt"
                    }
                </p>

                ${
                    station.employee_2
                    ? `
                    <p>
                        ${station.employee_2}
                    </p>
                    `
                    : ""
                }

                ${
                    station.double_takt_allowed
                    ? `
                    <small>
                        Doppeltakt möglich
                    </small>
                    `
                    : ""
                }

            </div>
        `;
    });

    document.getElementById(
        "rotation_result"
    ).innerText =
        JSON.stringify(
            data.support_employees,
            null,
            2
        );

    loadStats();
}


loadStats();

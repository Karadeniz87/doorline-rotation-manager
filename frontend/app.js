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
        console.error("Fehler beim Laden der KPIs:", error);
    }
}


async function runRotation() {

    try {

        const response = await fetch(
            "/rotation/run",
            {
                method: "POST"
            }
        );

        const data = await response.json();

        const stationsContainer =
            document.getElementById(
                "stations_container"
            );

        stationsContainer.innerHTML = "";

        data.stations.forEach(station => {

            stationsContainer.innerHTML += `
                <div class="station">

                    <h3>${station.name}</h3>

                    <p>
                        👤 ${
                            station.employee_1
                            ? station.employee_1
                            : "Nicht besetzt"
                        }
                    </p>

                    ${
                        station.employee_2
                        ? `
                        <p>
                            👤 ${station.employee_2}
                        </p>
                        `
                        : ""
                    }

                    ${
                        station.double_takt_allowed
                        ? `
                        <small>
                            🔵 Doppeltakt möglich
                        </small>
                        `
                        : ""
                    }

                    ${
                        station.support_required
                        ? `
                        <p style="color:red;">
                            Support benötigt
                        </p>
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

        result.innerText =
            JSON.stringify(
                data,
                null,
                2
            );

        loadStats();

    } catch (error) {

        console.error(
            "Rotation Fehler:",
            error
        );

        document.getElementById(
            "rotation_result"
        ).innerText =
            "Fehler bei der Rotation.";
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

        if (container.innerHTML !== "") {
            return;
        }

        stations.forEach(station => {

            container.innerHTML += `
                <div class="station">

                    <h3>${station.name}</h3>

                    <p>Nicht besetzt</p>

                    ${
                        station.double_takt_allowed
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

    } catch (error) {
        console.error(
            "Stationsfehler:",
            error
        );
    }
}


window.onload = function () {

    loadStats();

    loadStations();

};

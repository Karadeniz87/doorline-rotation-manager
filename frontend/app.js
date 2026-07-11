const API_URL = "https://doorline-rotation-manager.onrender.com";

async function loadDashboard() {
    await loadEmployees();
    await loadStations();
}

async function loadEmployees() {
    try {
        const response = await fetch(`${API_URL}/employees`);
        const employees = await response.json();

        document.getElementById("employees_total").innerText =
            employees.length;

        const available =
            employees.filter(
                e => e.status === "Verfügbar"
            ).length;

        const vacation =
            employees.filter(
                e => e.status === "Urlaub"
            ).length;

        const sick =
            employees.filter(
                e => e.status === "Krank"
            ).length;

        const support =
            employees.filter(
                e => e.status === "Support"
            ).length;

        document.getElementById("available").innerText =
            available;

        document.getElementById("vacation").innerText =
            vacation;

        document.getElementById("sick").innerText =
            sick;

        document.getElementById("support").innerText =
            support;

    } catch (error) {
        console.error(error);
    }
}

async function loadStations() {

    try {

        const response =
            await fetch(
                `${API_URL}/stations`
            );

        const stations =
            await response.json();

        const container =
            document.getElementById(
                "stations_container"
            );

        container.innerHTML = "";

        let doubleTaktCounter = 0;

        stations.forEach(station => {

            if (
                station.double_takt_active
            ) {
                doubleTaktCounter++;
            }

            const employee =
                station.employee_1 ||
                "Nicht besetzt";

            container.innerHTML += `
                <div class="station">
                    <h3>${station.name}</h3>
                    <p>${employee}</p>
                </div>
            `;
        });

        document.getElementById(
            "double_takt"
        ).innerText =
            doubleTaktCounter;

    } catch (error) {
        console.error(error);
    }
}

async function runRotation() {

    try {

        const response =
            await fetch(
                `${API_URL}/rotation/run`,
                {
                    method: "POST"
                }
            );

        const result =
            await response.json();

        document.getElementById(
            "rotation_result"
        ).innerText =
            JSON.stringify(
                result,
                null,
                2
            );

        await loadStations();

    } catch (error) {

        document.getElementById(
            "rotation_result"
        ).innerText =
            "Rotation Fehler";

        console.error(error);
    }
}

window.onload = () => {
    loadDashboard();
};

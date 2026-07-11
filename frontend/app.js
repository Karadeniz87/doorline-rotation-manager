const API_URL =
    "https://doorline-rotation-manager.onrender.com";


async function loadStats() {

    try {

        const response =
            await fetch(`${API_URL}/stats`);

        const data =
            await response.json();

        document.getElementById(
            "employees_total"
        ).innerText =
            data.employees_total || 0;

        document.getElementById(
            "available"
        ).innerText =
            data.available || 0;

        document.getElementById(
            "vacation"
        ).innerText =
            data.urlaub || 0;

        document.getElementById(
            "sick"
        ).innerText =
            data.krank || 0;

        document.getElementById(
            "support"
        ).innerText =
            data.support || 0;

        document.getElementById(
            "double_takt"
        ).innerText =
            data.double_takt || 0;

    } catch (error) {

        console.error(
            "Fehler beim Laden der KPI:",
            error
        );

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

        stations.forEach(station => {

            const employee =
                station.assigned_employee ||
                "Nicht besetzt";

            const support =
                station.support_required
                    ? "🔴 Support benötigt"
                    : "";

            container.innerHTML += `
                <div class="station">
                    <h3>${station.name}</h3>

                    <p>${employee}</p>

                    <p>${support}</p>

                </div>
            `;
        });

    } catch (error) {

        console.error(
            "Fehler beim Laden der Stationen:",
            error
        );

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
        await loadStats();

    } catch (error) {

        console.error(
            "Rotation Fehler:",
            error
        );

    }
}


window.onload = async () => {

    await loadStats();

    await loadStations();

};

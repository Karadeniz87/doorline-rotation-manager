const API_URL =
    "https://DEIN-RENDER-SERVICE.onrender.com";

async function loadStations() {

    const response =
        await fetch(`${API_URL}/stations`);

    const stations =
        await response.json();

    const container =
        document.getElementById(
            "stations_list"
        );

    container.innerHTML = "";

    stations.forEach(station => {

        const active =
            station.active
                ? "🟢 Aktiv"
                : "🔴 Deaktiviert";

        const doubleTakt =
            station.double_takt
                ? "⚡ Doppeltakt möglich"
                : "";

        container.innerHTML += `
            <div class="card">

                <h3>${station.name}</h3>

                <p>${active}</p>

                <p>${doubleTakt}</p>

                <button
                    onclick="
                        toggleStation(
                            '${station.name}',
                            ${station.active}
                        )
                    ">
                    ${
                        station.active
                        ? "Deaktivieren"
                        : "Aktivieren"
                    }
                </button>

            </div>
        `;
    });
}

async function toggleStation(
    stationName,
    active
) {

    const endpoint =
        active
        ? "deactivate"
        : "activate";

    await fetch(
        `${API_URL}/stations/${stationName}/${endpoint}`,
        {
            method: "PUT"
        }
    );

    loadStations();
}

loadStations();

const API =
    "https://doorline-rotation-manager.onrender.com";

async function loadStats() {
    const response = await fetch(`${API}/stats`);
    const data = await response.json();

    document.getElementById("employees_total").innerText =
        data.employees_total;

    document.getElementById("available").innerText =
        data.available;

    document.getElementById("vacation").innerText =
        data.urlaub;

    document.getElementById("sick").innerText =
        data.krank;

    document.getElementById("support").innerText =
        data.support ?? 0;
}

async function runRotation() {

    const response = await fetch(
        `${API}/rotation/run`,
        {
            method: "POST"
        }
    );

    const data = await response.json();

    document.getElementById(
        "rotation_result"
    ).innerText =
        JSON.stringify(data, null, 2);
}

loadStats();

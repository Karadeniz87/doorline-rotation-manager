const API =
    "https://DEIN-RENDER-SERVICE.onrender.com";

async function loadKPI() {

    const statsResponse =
        await fetch(`${API}/stats`);

    const stats =
        await statsResponse.json();

    document.getElementById("available").innerText =
        stats.available || 0;

    document.getElementById("vacation").innerText =
        stats.urlaub || 0;

    document.getElementById("sick").innerText =
        stats.krank || 0;

    document.getElementById("support").innerText =
        stats.support || 0;

    document.getElementById("double_takt").innerText =
        stats.double_takt || 0;


    const employeesResponse =
        await fetch(`${API}/employees`);

    const employees =
        await employeesResponse.json();

    employees.sort(
        (a, b) =>
            a.fairness_points -
            b.fairness_points
    );

    const fairness =
        document.getElementById(
            "fairness_ranking"
        );

    fairness.innerHTML = "";

    employees.forEach(employee => {

        let skillCount = 0;

        Object.keys(employee).forEach(key => {
            if (
                key.startsWith("skill_") &&
                employee[key]
            ) {
                skillCount++;
            }
        });

        fairness.innerHTML += `
            <div class="station">
                ${employee.firstname}
                ${employee.lastname}
                -
                Fairness:
                ${employee.fairness_points || 0}
            </div>
        `;

        document.getElementById(
            "flexibility_ranking"
        ).innerHTML += `
            <div class="station">
                ${employee.firstname}
                ${employee.lastname}
                -
                Skills:
                ${skillCount}
            </div>
        `;
    });
}

loadKPI();

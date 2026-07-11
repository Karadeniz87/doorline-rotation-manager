const api =
"https://doorline-rotation-manager.onrender.com";

document
.getElementById("rotationButton")
.addEventListener("click", async () => {

    const response = await fetch(
        `${api}/rotation/run`,
        {
            method:"POST"
        }
    );

    const data = await response.json();

    document
    .getElementById("rotationResult")
    .innerHTML =
    JSON.stringify(data,null,2);
});

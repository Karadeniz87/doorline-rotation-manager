async function login() {

    const response = await fetch(
        "/login",
        {
            method: "POST",
            headers: {
                "Content-Type":
                    "application/json"
            },
            body: JSON.stringify({
                username:
                    document.getElementById(
                        "username"
                    ).value,

                password:
                    document.getElementById(
                        "password"
                    ).value
            })
        }
    );

    const data = await response.json();

    if (response.ok) {

        localStorage.setItem(
            "user",
            JSON.stringify(data)
        );

        window.location.href = "/";
    }

    else {
        alert(data.detail);
    }
}

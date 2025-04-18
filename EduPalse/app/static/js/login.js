document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");

    loginForm.addEventListener("submit", function (event) {
        event.preventDefault(); // Prevent default form submission

        const idNumber = document.getElementById("id_number").value.trim();
        const password = document.getElementById("password").value.trim();

        if (idNumber === "" || password === "") {
            alert("Please fill in all fields!");
            return;
        }

        fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ id_number: idNumber, password: password })
        })
        .then(async response => {
            // Try to parse JSON even if response is not 200
            const data = await response.json();
            if (!response.ok) {
                throw new Error(data.message || "Login failed");
            }
            return data;
        })
        .then(data => {
            if (data.status === "success") {
                const role = data.user_type;

                if (role === "Student") {
                    window.location.href = "/student_home";
                } else if (role === "Teacher") {
                    window.location.href = "/teacher_home";
                } else if (role === "Admin") {
                    window.location.href = "/admin_home";
                } else if (role === "Parent") {
                    window.location.href = "/parent_home";
                } else {
                    alert("User type not recognized");
                }
            } else {
                alert("Invalid login credentials!");
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert(error.message);  // More descriptive alert
        });
    });
});

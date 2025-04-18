document.addEventListener("DOMContentLoaded", function () {
    const userType = document.getElementById("user_type");
    const studentFields = document.getElementById("student-fields");
    const teacherFields = document.getElementById("teacher-fields");
    const parentFields = document.getElementById("parent-fields");
    const adminFields = document.getElementById("admin-fields");

    const classSelection = document.getElementById("class");
    const groupSelection = document.getElementById("group-selection");
    const generatedIdSelect = document.getElementById("unique_id");

    //const childIdInput = document.getElementById("child_unique_id");
    //const validationMsg = document.getElementById("child-id-validation-msg");
    //alert(childIdInput);

    // Utility function to set required attributes dynamically
    function setRequired(fields, required) {
        fields.forEach(field => {
            if (required) {
                field.setAttribute("required", "required");
            } else {
                field.removeAttribute("required");
            }
        });
    }

    // Show/hide and validate based on user type
    userType.addEventListener("change", function () {
        const selectedType = userType.value;

        // Hide all
        studentFields.classList.add("hidden");
        teacherFields.classList.add("hidden");
        parentFields.classList.add("hidden");
        adminFields.classList.add("hidden");

        // Remove all required fields first
        setRequired(document.querySelectorAll('#student-fields input, #teacher-fields input, #parent-fields input, #admin-fields input'), false);

        // Show relevant section and add required fields
        if (selectedType === "Student") {
            studentFields.classList.remove("hidden");
            setRequired(document.querySelectorAll('#student-fields input'), true);
        } else if (selectedType === "Teacher") {
            teacherFields.classList.remove("hidden");
            setRequired(document.querySelectorAll('#teacher-fields input'), true);
        } else if (selectedType === "Parent") {
            parentFields.classList.remove("hidden");
            setRequired(document.querySelectorAll('#parent-fields input'), true);
        } else if (selectedType === "Admin") {
            adminFields.classList.remove("hidden");
            setRequired(document.querySelectorAll('#admin-fields input'), true);
        }
    });

    // Show group selection if class is 11 or 12
    if (classSelection) {
        classSelection.addEventListener("change", function () {
            if (classSelection.value === "11" || classSelection.value === "12") {
                groupSelection.classList.remove("hidden");
            } else {
                groupSelection.classList.add("hidden");
            }
        });
    }

    // Generate 5 random 8-digit IDs and populate dropdown
    function generateIds() {
        if (generatedIdSelect) {
            generatedIdSelect.innerHTML = "";
            for (let i = 0; i < 5; i++) {
                let id = Math.floor(10000000 + Math.random() * 90000000);
                let option = document.createElement("option");
                option.value = id;
                option.textContent = id;
                generatedIdSelect.appendChild(option);
            }
        }
    }

    generateIds(); // Generate IDs on page load

    // Password match validation
    document.getElementById("signup-form").addEventListener("submit", function (event) {
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm_password").value;
        if (password !== confirmPassword) {
            event.preventDefault();
            alert("Passwords do not match!");
        }
    });

    // Child ID validation with AJAX
    /*if (childIdInput) {
        childIdInput.addEventListener("blur", function () {
            const childId = childIdInput.value.trim();
            if (childId) {
                fetch(`/check-child-id/${childId}`)
                    .then(response => response.json())
                    .then(data => {
                        if (!data.exists) {
                            validationMsg.style.display = "block";
                            validationMsg.textContent = "Child Unique ID not found. Please enter a valid ID.";
                        } else {
                            validationMsg.style.display = "none";
                            validationMsg.textContent = "";
                        }
                    })
                    .catch(() => {
                        validationMsg.style.display = "block";
                        validationMsg.textContent = "Error checking Child ID.";
                    });
            } else {
                validationMsg.style.display = "none";
                validationMsg.textContent = "";
            }
        });
    }*/
});

document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const form = document.getElementById('signup-form');
    const userTypeCards = document.querySelectorAll('.user-type-card');
    const userTypeInput = document.getElementById('user_type');
    const dynamicFieldsContainer = document.getElementById('dynamic-fields-container');
    const formSteps = document.querySelectorAll('.form-step');
    const nextButtons = document.querySelectorAll('.btn-next');
    const backButtons = document.querySelectorAll('.btn-back');
    const submitButton = document.querySelector('.btn-submit');
    const progressBar = document.getElementById('formProgress');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const loadingOverlay = document.getElementById('loadingOverlay');
    const confirmationModal = document.getElementById('confirmationModal');
    const confirmationContent = document.getElementById('confirmationContent');
    const modalClose = document.querySelector('.modal-close');
    const btnCancel = document.querySelector('.btn-cancel');
    const btnConfirm = document.querySelector('.btn-confirm');
    const generatedIdSelect = document.getElementById('unique_id');

    // Form data storage
    let formData = {
        user_type: '',
        student: {},
        teacher: {},
        parent: {},
        admin: {},
        account: {}
    };

    // Generate IDs function
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

    // Templates for dynamic fields
    const fieldTemplates = {
        Student: `
            <div class="form-group">
                <label for="student_name"><i class="fas fa-user"></i> Student Name</label>
                <input type="text" id="student_name" name="student_name" required>
                <div class="input-feedback"></div>
            </div>
            <div class="form-group">
                <label for="roll_number"><i class="fas fa-id-badge"></i> Roll Number</label>
                <input type="text" id="roll_number" name="roll_number" required>
                <div class="input-feedback"></div>
            </div>
            <div class="form-group">
                <label for="esim_number"><i class="fas fa-qrcode"></i> ESIM Number</label>
                <input type="text" id="esim_number" name="esim_number" required>
                <div class="input-feedback"></div>
            </div>
            <div class="form-group">
                <label for="class"><i class="fas fa-school"></i> Class</label>
                <select id="class" name="class" required>
                    <option value="">Select Class</option>
                    ${Array.from({length: 12}, (_, i) => `<option value="${i+1}">${i+1}</option>`).join('')}
                    <option value="other">Other</option>
                </select>
                <div class="input-feedback"></div>
            </div>
            <div class="form-group hidden" id="group-selection">
                <label for="group"><i class="fas fa-users"></i> Select Group</label>
                <select id="group" name="group">
                    <option value="">Select Group</option>
                    <option value="Science">Science</option>
                    <option value="Commerce">Commerce</option>
                    <option value="Arts">Arts</option>
                </select>
                <div class="input-feedback"></div>
            </div>
            <div class="form-group">
                <label for="section"><i class="fas fa-users"></i> Section</label>
                <input type="text" id="section" name="section" required>
                <div class="input-feedback"></div>
            </div>
        `,
        Teacher: `
            <div class="form-group">
                <label for="teacher_name"><i class="fas fa-user"></i> Teacher Name</label>
                <input type="text" id="teacher_name" name="teacher_name" required>
                <div class="input-feedback"></div>
            </div>
            <div class="form-group">
                <label for="attending_classes"><i class="fas fa-chalkboard"></i> Attending Classes & Sections</label>
                <input type="text" id="attending_classes" name="attending_classes" placeholder="Example: 9A, 10B" required>
                <div class="input-feedback"></div>
            </div>
        `,
        Parent: `
            <div class="form-group">
                <label for="parent_name"><i class="fas fa-user"></i> Parent Name</label>
                <input type="text" id="parent_name" name="parent_name" required>
                <div class="input-feedback"></div>
            </div>
            <div class="form-group">
                <label for="child_name"><i class="fas fa-child"></i> Child Name</label>
                <input type="text" id="child_name" name="child_name" required>
                <div class="input-feedback"></div>
            </div>
            <div class="form-group">
                <label for="child_class"><i class="fas fa-school"></i> Child Class</label>
                <input type="text" id="child_class" name="child_class" required>
                <div class="input-feedback"></div>
            </div>
            <div class="form-group">
                <label for="child_section"><i class="fas fa-users"></i> Child Section</label>
                <input type="text" id="child_section" name="child_section" required>
                <div class="input-feedback"></div>
            </div>
            <div class="form-group">
                <label for="child_unique_id"><i class="fas fa-id-card"></i> Child Unique ID</label>
                <input type="text" id="child_unique_id" name="child_unique_id" required>
                <div class="input-feedback"></div>
            </div>
        `,
        Admin: `
            <div class="form-group">
                <label for="admin_name"><i class="fas fa-user"></i> Admin Name</label>
                <input type="text" id="admin_name" name="admin_name" required>
                <div class="input-feedback"></div>
            </div>
        `
    };

    // Initialize form
    initForm();

    function initForm() {
        // Generate IDs on page load
        generateIds();

        // Set up user type selection
        userTypeCards.forEach(card => {
            card.addEventListener('click', function() {
                userTypeCards.forEach(c => c.classList.remove('selected'));
                this.classList.add('selected');
                const userType = this.dataset.value;
                userTypeInput.value = userType;
                formData.user_type = userType;
                
                // Enable next button
                document.querySelector('.btn-next').disabled = false;
            });
        });

        // Set up form navigation
        nextButtons.forEach(button => {
            button.addEventListener('click', function() {
                const currentStep = this.closest('.form-step');
                const currentStepNumber = parseInt(currentStep.dataset.step);
                
                if (validateStep(currentStepNumber)) {
                    // Save step data
                    saveStepData(currentStepNumber);
                    
                    // Show next step
                    showStep(currentStepNumber + 1);
                    
                    // Update progress bar
                    updateProgressBar(currentStepNumber + 1);
                }
            });
        });

        backButtons.forEach(button => {
            button.addEventListener('click', function() {
                const currentStep = this.closest('.form-step');
                const currentStepNumber = parseInt(currentStep.dataset.step);
                
                // Show previous step
                showStep(currentStepNumber - 1);
                
                // Update progress bar
                updateProgressBar(currentStepNumber - 1);
            });
        });

        // Password toggle
        document.querySelectorAll('.toggle-password').forEach(toggle => {
            toggle.addEventListener('click', function() {
                const input = this.previousElementSibling;
                const type = input.getAttribute('type') === 'password' ? 'text' : 'password';
                input.setAttribute('type', type);
                this.classList.toggle('fa-eye-slash');
            });
        });

        // Password strength check
        passwordInput.addEventListener('input', checkPasswordStrength);

        // Class selection for students
        document.addEventListener('change', function(e) {
            if (e.target.id === 'class' && formData.user_type === 'Student') {
                const classValue = e.target.value;
                const groupSelection = document.getElementById('group-selection');
                
                if (groupSelection) {
                    if (['11', '12'].includes(classValue)) {
                        groupSelection.classList.remove('hidden');
                    } else {
                        groupSelection.classList.add('hidden');
                    }
                }
            }
        });

        // Form submission
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            if (validateStep(3)) {
                // Save final step data
                saveStepData(3);
                
                // Show confirmation modal
                showConfirmationModal();
            }
        });

        // Modal controls
        modalClose.addEventListener('click', closeModal);
        btnCancel.addEventListener('click', closeModal);
        btnConfirm.addEventListener('click', submitForm);
    }

    function validateStep(stepNumber) {
        let isValid = true;
        
        if (stepNumber === 1) {
            if (!formData.user_type) {
                isValid = false;
                // Show error on user type selection
                const errorElement = document.querySelector('.user-type-selector');
                if (errorElement) {
                    errorElement.insertAdjacentHTML('afterend', '<div class="input-feedback" style="display: block;">Please select a user type</div>');
                }
            }
        } else if (stepNumber === 2) {
            // Validate role-specific fields
            const inputs = dynamicFieldsContainer.querySelectorAll('input[required], select[required]');
            inputs.forEach(input => {
                if (!input.value.trim()) {
                    isValid = false;
                    showError(input, 'This field is required');
                } else {
                    showSuccess(input);
                }
            });
        } else if (stepNumber === 3) {
            // Validate account fields
            const emailInput = document.getElementById('email');
            const phoneInput = document.getElementById('phone');
            const uniqueIdInput = document.getElementById('unique_id');
            
            // Email validation
            if (!emailInput.value.trim()) {
                isValid = false;
                showError(emailInput, 'Email is required');
            } else if (!isValidEmail(emailInput.value.trim())) {
                isValid = false;
                showError(emailInput, 'Please enter a valid email');
            } else {
                showSuccess(emailInput);
            }
            
            // Phone validation
            if (!phoneInput.value.trim()) {
                isValid = false;
                showError(phoneInput, 'Phone number is required');
            } else if (!isValidPhone(phoneInput.value.trim())) {
                isValid = false;
                showError(phoneInput, 'Please enter a valid phone number');
            } else {
                showSuccess(phoneInput);
            }
            
            // Unique ID validation
            if (!uniqueIdInput.value) {
                isValid = false;
                showError(uniqueIdInput, 'Please select an ID');
            } else {
                showSuccess(uniqueIdInput);
            }
            
            // Password validation
            if (!passwordInput.value) {
                isValid = false;
                showError(passwordInput, 'Password is required');
            } else if (passwordInput.value.length < 8) {
                isValid = false;
                showError(passwordInput, 'Password must be at least 8 characters');
            } else {
                showSuccess(passwordInput);
            }
            
            // Confirm password validation
            if (!confirmPasswordInput.value) {
                isValid = false;
                showError(confirmPasswordInput, 'Please confirm your password');
            } else if (confirmPasswordInput.value !== passwordInput.value) {
                isValid = false;
                showError(confirmPasswordInput, 'Passwords do not match');
            } else {
                showSuccess(confirmPasswordInput);
            }
        }
        
        return isValid;
    }

    function showStep(stepNumber) {
        // Hide all steps
        formSteps.forEach(step => {
            step.classList.remove('active');
        });
        
        // Show current step
        const currentStep = document.querySelector(`.form-step[data-step="${stepNumber}"]`);
        if (currentStep) {
            currentStep.classList.add('active');
        }
        
        // Update button visibility
        const backButton = document.querySelector('.btn-back');
        const nextButton = document.querySelector('.btn-next');
        
        if (stepNumber === 1) {
            if (backButton) backButton.style.display = 'none';
        } else {
            if (backButton) backButton.style.display = 'inline-block';
        }
        
        if (stepNumber === 3) {
            if (nextButton) nextButton.style.display = 'none';
            if (submitButton) submitButton.style.display = 'inline-block';
        } else {
            if (nextButton) nextButton.style.display = 'inline-block';
            if (submitButton) submitButton.style.display = 'none';
        }
        
        // Load dynamic fields when moving to step 2
        if (stepNumber === 2 && formData.user_type) {
            loadDynamicFields(formData.user_type);
        }
    }

    function loadDynamicFields(userType) {
        if (fieldTemplates[userType]) {
            dynamicFieldsContainer.innerHTML = fieldTemplates[userType];
        }
    }

    function saveStepData(stepNumber) {
        if (stepNumber === 1) {
            // User type is already saved when selected
            return;
        }
        
        if (stepNumber === 2) {
            const inputs = dynamicFieldsContainer.querySelectorAll('input, select');
            inputs.forEach(input => {
                formData[formData.user_type.toLowerCase()][input.name] = input.value;
            });
        }
        
        if (stepNumber === 3) {
            formData.account = {
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                unique_id: document.getElementById('unique_id').value,
                password: passwordInput.value
            };
        }
    }

    function updateProgressBar(stepNumber) {
        const progress = (stepNumber / formSteps.length) * 100;
        progressBar.style.transform = `scaleX(${progress / 100})`;
    }

    function checkPasswordStrength() {
        const password = passwordInput.value;
        const strengthText = document.getElementById('passwordStrength');
        
        if (!password) {
            strengthText.textContent = '';
            strengthText.className = '';
            return;
        }
        
        let strength = 0;
        
        // Length
        if (password.length >= 8) strength += 1;
        if (password.length >= 12) strength += 1;
        
        // Contains numbers
        if (/\d/.test(password)) strength += 1;
        
        // Contains lowercase and uppercase
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength += 1;
        
        // Contains special chars
        if (/[^a-zA-Z0-9]/.test(password)) strength += 1;
        
        // Update text
        switch (strength) {
            case 0:
            case 1:
                strengthText.textContent = 'Very Weak';
                strengthText.className = 'weak';
                break;
            case 2:
                strengthText.textContent = 'Weak';
                strengthText.className = 'weak';
                break;
            case 3:
                strengthText.textContent = 'Moderate';
                strengthText.className = 'moderate';
                break;
            case 4:
                strengthText.textContent = 'Strong';
                strengthText.className = 'strong';
                break;
            case 5:
                strengthText.textContent = 'Very Strong';
                strengthText.className = 'strong';
                break;
        }
    }

    function showError(input, message) {
        const formGroup = input.closest('.form-group');
        const feedback = formGroup.querySelector('.input-feedback');
        
        if (feedback) {
            formGroup.classList.add('error');
            feedback.textContent = message;
            feedback.style.opacity = '1';
        }
    }

    function showSuccess(input) {
        const formGroup = input.closest('.form-group');
        const feedback = formGroup.querySelector('.input-feedback');
        
        if (feedback) {
            formGroup.classList.remove('error');
            feedback.style.opacity = '0';
        }
    }

    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    function isValidPhone(phone) {
        return /^[0-9]{10,15}$/.test(phone);
    }

    function showConfirmationModal() {
        // Prepare confirmation content based on user type
        let content = `
            <h4>Please confirm your details</h4>
            <div class="confirmation-section">
                <h5>Account Type</h5>
                <p><strong>User Type:</strong> ${formData.user_type}</p>
            </div>
        `;
        
        // Add role-specific details
        const roleData = formData[formData.user_type.toLowerCase()];
        content += `<div class="confirmation-section"><h5>${formData.user_type} Information</h5>`;
        for (const [key, value] of Object.entries(roleData)) {
            content += `<p><strong>${key.replace('_', ' ')}:</strong> ${value || 'Not provided'}</p>`;
        }
        content += `</div>`;
        
        // Add account details
        content += `
            <div class="confirmation-section">
                <h5>Account Information</h5>
                <p><strong>Email:</strong> ${formData.account.email}</p>
                <p><strong>Phone:</strong> ${formData.account.phone}</p>
                <p><strong>Generated ID:</strong> ${formData.account.unique_id}</p>
            </div>
        `;
        
        confirmationContent.innerHTML = content;
        confirmationModal.classList.add('active');
    }

    function closeModal() {
        confirmationModal.classList.remove('active');
    }

    function submitForm() {
        loadingOverlay.classList.add('active');
        
        // Simulate API call with timeout
        setTimeout(() => {
            loadingOverlay.classList.remove('active');
            closeModal();
            
            // Show success message
            alert('Registration successful! You will receive a confirmation email shortly.');
            
            // Reset form
            form.reset();
            formData = {
                user_type: '',
                student: {},
                teacher: {},
                parent: {},
                admin: {},
                account: {}
            };
            
            // Reset UI
            userTypeCards.forEach(card => card.classList.remove('selected'));
            dynamicFieldsContainer.innerHTML = '';
            showStep(1);
            updateProgressBar(1);
            generateIds(); // Generate new IDs
        }, 2000);
    }
});

document.querySelector('.btn-confirm').addEventListener('click', function() {
    document.getElementById('signup-form').submit();
});

document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const loginForm = document.getElementById('loginForm');
    const idNumberInput = document.getElementById('id_number');
    const passwordInput = document.getElementById('password');
    const togglePassword = document.querySelector('.toggle-password');
    const loadingOverlay = document.getElementById('loadingOverlay');
    
    // Close flash messages
    document.querySelectorAll('.close-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            this.parentElement.style.opacity = '0';
            setTimeout(() => {
                this.parentElement.remove();
            }, 300);
        });
    });
    
    // Auto-close success messages after 5 seconds
    const successMessages = document.querySelectorAll('.alert.success');
    successMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            setTimeout(() => {
                msg.remove();
            }, 300);
        }, 5000);
    });
    
    // Toggle password visibility
    if (togglePassword) {
        togglePassword.addEventListener('click', function() {
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            this.classList.toggle('fa-eye-slash');
        });
    }
    
    // Form validation
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Validate ID Number
            if (!idNumberInput.value.trim()) {
                showError(idNumberInput, 'ID Number is required');
                isValid = false;
            } else if (!/^\d+$/.test(idNumberInput.value.trim())) {
                showError(idNumberInput, 'ID Number should contain only numbers');
                isValid = false;
            } else {
                showSuccess(idNumberInput);
            }
            
            // Validate Password
            if (!passwordInput.value.trim()) {
                showError(passwordInput, 'Password is required');
                isValid = false;
            } /*else if (passwordInput.value.trim().length > 0) {
                showError(passwordInput, 'Passwords must be at least 6 characters');
                isValid = false;
            }*/ else {
                showSuccess(passwordInput);
            }
            
            if (!isValid) {
                e.preventDefault();
            } else {
                // Show loading spinner
                loadingOverlay.classList.add('active');
                document.querySelector('.btn-login .btn-text').textContent = 'Logging in...';
                document.querySelector('.btn-login .loader').style.opacity = '1';
            }
        });
    }
    
    // Input validation on blur
    idNumberInput.addEventListener('blur', validateIdNumber);
    passwordInput.addEventListener('blur', validatePassword);
    
    // Real-time validation while typing
    idNumberInput.addEventListener('input', function() {
        if (this.value.trim()) {
            showSuccess(this);
        }
    });
    
    passwordInput.addEventListener('input', function() {
        if (this.value.trim() && this.value.trim().length >= 6) {
            showSuccess(this);
        }
    });
    
    // Validation functions
    function validateIdNumber() {
        const value = idNumberInput.value.trim();
        if (!value) {
            showError(idNumberInput, 'ID Number is required');
            return false;
        }
        if (!/^\d+$/.test(value)) {
            showError(idNumberInput, 'ID Number should contain only numbers');
            return false;
        }
        showSuccess(idNumberInput);
        return true;
    }
    
    function validatePassword() {
        const value = passwordInput.value.trim();
        if (!value) {
            showError(passwordInput, 'Password is required');
            return false;
        }
        /*if (value.length < 6>) {
            showError(passwordInput, 'Password must be at least 6 characters');
            return false;
        }*/
        showSuccess(passwordInput);
        return true;
    }
    
    // Helper functions
    function showError(input, message) {
        const formGroup = input.closest('.form-group');
        const feedback = formGroup.querySelector('.input-feedback');
        feedback.textContent = message;
        feedback.style.opacity = '1';
        formGroup.classList.add('error');
    }
    
    function showSuccess(input) {
        const formGroup = input.closest('.form-group');
        const feedback = formGroup.querySelector('.input-feedback');
        feedback.style.opacity = '0';
        formGroup.classList.remove('error');
    }
    
    // Add ripple effect to buttons
    document.querySelectorAll('.btn-login, .social-btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 1000);
        });
    });
});
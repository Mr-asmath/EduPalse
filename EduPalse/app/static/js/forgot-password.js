document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const forgotForm = document.getElementById('forgotForm');
    const emailInput = document.getElementById('email');
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
    
    // Form validation
    if (forgotForm) {
        forgotForm.addEventListener('submit', function(e) {
            if (!validateEmail()) {
                e.preventDefault();
            } else {
                // Show loading spinner
                loadingOverlay.classList.add('active');
                document.querySelector('.btn-reset .btn-text').textContent = 'Sending...';
                document.querySelector('.btn-reset .loader').style.opacity = '1';
            }
        });
    }
    
    // Input validation on blur
    emailInput.addEventListener('blur', validateEmail);
    
    // Real-time validation while typing
    emailInput.addEventListener('input', function() {
        if (this.value.trim() && isValidEmail(this.value.trim())) {
            showSuccess(this);
        }
    });
    
    // Validation functions
    function validateEmail() {
        const value = emailInput.value.trim();
        if (!value) {
            showError(emailInput, 'Email is required');
            return false;
        }
        if (!isValidEmail(value)) {
            showError(emailInput, 'Please enter a valid email address');
            return false;
        }
        showSuccess(emailInput);
        return true;
    }
    
    function isValidEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
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
    
    // Add ripple effect to button
    const resetButton = document.querySelector('.btn-reset');
    if (resetButton) {
        resetButton.addEventListener('click', function(e) {
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
    }
});
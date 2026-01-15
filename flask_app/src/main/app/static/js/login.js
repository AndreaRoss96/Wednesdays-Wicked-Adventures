document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // DOM Elements 
    // ============================================
    const loginForm = document.getElementById('loginForm');
    const loginButton = document.getElementById('loginSubmitButton');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    
    // ============================================
    // SVG Icons Configuration
    // ============================================
    const svgIcons = {
        eyeOpen: `
            <path d="M12 15a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z" />
            <path fill-rule="evenodd" d="M1.323 11.447C2.811 6.976 7.028 3.75 12.001 3.75c4.97 0 9.185 3.223 10.675 7.69.12.362.12.752 0 1.113-1.487 4.471-5.705 7.697-10.677 7.697-4.97 0-9.186-3.223-10.675-7.69a1.762 1.762 0 0 1 0-1.113ZM17.25 12a5.25 5.25 0 1 1-10.5 0 5.25 5.25 0 0 1 10.5 0Z" clip-rule="evenodd" />
        `,
        eyeClosed: `
            <path fill-rule="evenodd" d="M3.53 2.47a.75.75 0 0 0-1.06 1.06l18 18a.75.75 0 1 0 1.06-1.06l-18-18ZM22.676 12.553a11.249 11.249 0 0 1-2.631 4.31l-3.099-3.099a5.25 5.25 0 0 0-6.71-6.71L7.759 4.577a11.217 11.217 0 0 1 4.242-.827c4.97 0 9.185 3.223 10.675 7.69.12.362.12.752 0 1.113Z" clip-rule="evenodd" />
            <path d="M15.75 12c0 .18-.013.357-.037.53l-4.244-4.243A3.75 3.75 0 0 1 15.75 12Z" />
            <path d="M6.75 12c0-.619.107-1.213.304-1.764l-3.1-3.1a11.25 11.25 0 0 0-2.63 4.31c-.12.362-.12.752 0 1.114 1.489 4.476 5.704 7.69 10.675 7.69 1.5 0 2.933-.294 4.242-.827l-2.477-2.477A5.25 5.25 0 0 1 6.75 12Z" />
        `,
        errorIcon: `
            <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12ZM12 8.25a.75.75 0 0 1 .75.75v3.75a.75.75 0 0 1-1.5 0V9a.75.75 0 0 1 .75-.75Zm0 8.25a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Z" clip-rule="evenodd" />
        `
    };
    
    // ============================================
    // Constants
    // ============================================
    const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // ============================================
    // Form Validation Functions
    // ============================================
    function validateForm(email, password) {
        // Check for empty fields
        if (!email || !password) {
            return { isValid: false, message: 'Please fill in all fields.' };
        }
        
        // Validate email format
        if (!EMAIL_REGEX.test(email)) {
            return { isValid: false, message: 'Please enter a valid email address.' };
        }
        
        return { isValid: true };
    }

    // ============================================
    // UI State Management
    // ============================================
    function showLoadingState() {
        if (loginButton) {
            loginButton.disabled = true;
            loginButton.textContent = 'Signing in...';
        }
    }

    function resetLoadingState() {
        if (loginButton) {
            loginButton.disabled = false;
            loginButton.textContent = 'Sign In';
        }
    }

    // ============================================
    // Error Handling
    // ============================================
    function showError(message) {
        // Remove existing error messages
        removeExistingErrors();
        
        // Create error element
        const errorDiv = document.createElement('div');
        errorDiv.className = 'auth-message error';
        errorDiv.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                ${svgIcons.errorIcon}
            </svg>
            <span>${message}</span>
        `;
        
        // Insert error message before the form
        const form = document.querySelector('.auth-form');
        if (form) {
            form.parentNode.insertBefore(errorDiv, form);
        }
    }

    function removeExistingErrors() {
        const existingErrors = document.querySelectorAll('.auth-message.error');
        existingErrors.forEach(error => error.remove());
    }

    // ============================================
    // Form Submission Handler
    // ============================================
    function handleFormSubmit(e) {
        e.preventDefault();
        
        // Get form values
        const email = emailInput.value.trim();
        const password = passwordInput.value.trim();
    
        // Validate form
        const validation = validateForm(email, password);
        if (!validation.isValid) {
            showError(validation.message);
            return;
        }
        
        // Show loading state
        showLoadingState();
        
        // Submit the form 
        loginForm.submit();
        
        // Reset button state after 3 seconds (fallback)
        setTimeout(() => {
            resetLoadingState();
        }, 3000);
    }

    // ============================================
    // Input Event Listeners
    // ============================================
    function setupInputValidation() {
        // Clear errors when user starts typing
        [emailInput, passwordInput].forEach(input => {
            if (input) {
                input.addEventListener('input', function() {
                    removeExistingErrors();
                });
            }
        });
    }

    // ============================================
    // Initialization
    // ============================================
    function initialize() {
        // Setup form submission
        if (loginForm) {
            loginForm.addEventListener('submit', handleFormSubmit);
        }
        
        // Setup input validation listeners
        setupInputValidation();
        
        // Focus on email input for better UX
        if (emailInput) {
            emailInput.focus();
        }
    }

    // ============================================
    // Start Application
    // ============================================
    initialize();
});
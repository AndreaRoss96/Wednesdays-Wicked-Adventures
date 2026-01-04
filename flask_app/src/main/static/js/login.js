document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // DOM Elements
    // ============================================
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');
    const eyeIcon = document.getElementById('eyeIcon');
    const loginForm = document.getElementById('loginForm');
    const loginButton = loginForm?.querySelector('.login-button');
    const buttonText = document.getElementById('buttonText');
    const loadingSpinner = document.getElementById('loadingSpinner');
    
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
            <path d="M15.75 12c0 .18-.013.357-.037.53l-4.244-4.243A3.75 3.75 0 0 1 15.75 12ZM12.53 15.713l-4.243-4.244a3.75 3.75 0 0 0 4.244 4.243Z" />
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
    const SIMULATION_DELAY = 1500; // milliseconds

    // ============================================
    // Password Toggle Functionality
    // ============================================
    function initializePasswordToggle() {
        if (!togglePassword || !passwordInput || !eyeIcon) return;
        
        togglePassword.addEventListener('click', function() {
            const isPassword = passwordInput.getAttribute('type') === 'password';
            const newType = isPassword ? 'text' : 'password';
            
            // Toggle input type
            passwordInput.setAttribute('type', newType);
            
            // Update eye icon
            eyeIcon.innerHTML = isPassword ? svgIcons.eyeClosed : svgIcons.eyeOpen;
        });
    }

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
        if (!loginButton || !buttonText || !loadingSpinner) return;
        
        loginButton.disabled = true;
        buttonText.textContent = 'Signing in...';
        loadingSpinner.style.display = 'inline-block';
    }

    function resetLoadingState() {
        if (!loginButton || !buttonText || !loadingSpinner) return;
        
        loginButton.disabled = false;
        buttonText.textContent = 'Sign In';
        loadingSpinner.style.display = 'none';
    }

    // ============================================
    // Error Handling
    // ============================================
    function showError(message) {
        // Remove existing error messages
        removeExistingErrors();
        
        // Create error element
        const errorDiv = document.createElement('div');
        errorDiv.className = 'form-error';
        errorDiv.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                ${svgIcons.errorIcon}
            </svg>
            <span>${message}</span>
        `;
        
        // Insert error message after form header
        const formHeader = document.querySelector('.form-header');
        if (formHeader) {
            formHeader.parentNode.insertBefore(errorDiv, formHeader.nextSibling);
        }
        
        // Scroll to error for better user experience
        errorDiv.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
    }

    function removeExistingErrors() {
        const existingErrors = document.querySelectorAll('.form-error');
        existingErrors.forEach(error => error.remove());
    }

    // ============================================
    // Form Submission Handler
    // ============================================
    function handleFormSubmit(e) {
        e.preventDefault();
        
        // Get form values
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        // Validate form
        const validation = validateForm(email, password);
        if (!validation.isValid) {
            showError(validation.message);
            return;
        }
        
        // Show loading state
        showLoadingState();
        
        // Simulate API call
        simulateLoginRequest(email, password);
    }

    // ============================================
    // API Simulation (Replace with actual API call)
    // ============================================
    function simulateLoginRequest(email, password) {
        console.log('Login attempt with:', { email, password });
        
        // Simulate network delay
        setTimeout(() => {
            // In production, replace with actual authentication logic
            // For demo purposes, simulate successful login
            
            // Redirect to dashboard (simulated)
            // window.location.href = '/dashboard';
            
            // Reset button state (in case redirect fails)
            resetLoadingState();
        }, SIMULATION_DELAY);
    }

    // ============================================
    // Input Event Listeners
    // ============================================
    function setupInputValidation() {
        const emailInput = document.getElementById('email');
        const passwordInputField = document.getElementById('password');
        
        // Clear errors when user starts typing
        [emailInput, passwordInputField].forEach(input => {
            if (input) {
                input.addEventListener('input', function() {
                    removeExistingErrors();
                });
            }
        });
    }

    // ============================================
    // Accessibility Enhancements
    // ============================================
    function enhanceAccessibility() {
        // Add ARIA labels to password toggle
        if (togglePassword) {
            togglePassword.setAttribute('aria-label', 'Toggle password visibility');
            togglePassword.setAttribute('aria-pressed', 'false');
            
            // Update aria-pressed attribute when toggling
            togglePassword.addEventListener('click', function() {
                const isPressed = this.getAttribute('aria-pressed') === 'true';
                this.setAttribute('aria-pressed', (!isPressed).toString());
            });
        }
        
        // Add keyboard support for password toggle
        if (togglePassword) {
            togglePassword.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.click();
                }
            });
        }
    }

    // ============================================
    // Initialization
    // ============================================
    function initialize() {
        // Initialize password toggle
        initializePasswordToggle();
        
        // Setup form submission
        if (loginForm) {
            loginForm.addEventListener('submit', handleFormSubmit);
        }
        
        // Setup accessibility features
        enhanceAccessibility();
        
        // Setup input validation listeners
        setupInputValidation();
        
        // Focus on email input for better UX
        const emailInput = document.getElementById('email');
        if (emailInput) {
            emailInput.focus();
        }
    }

    // ============================================
    // Start Application
    // ============================================
    initialize();
});
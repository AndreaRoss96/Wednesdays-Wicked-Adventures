// ============================================
// DOM Elements
// ============================================
document.addEventListener('DOMContentLoaded', function() {
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');
    const eyeIcon = document.getElementById('eyeIcon');
    const loginForm = document.getElementById('loginForm');
    const contactForm = document.getElementById('contactForm');
    const loginButton = loginForm?.querySelector('.auth-submit-button');

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
        `,
        successIcon: `
            <path fill-rule="evenodd" d="M2.25 12c0-5.385 4.365-9.75 9.75-9.75s9.75 4.365 9.75 9.75-4.365 9.75-9.75 9.75S2.25 17.385 2.25 12Zm13.36-1.814a.75.75 0 1 0-1.22-.872l-3.236 4.53L9.53 12.22a.75.75 0 0 0-1.06 1.06l2.25 2.25a.75.75 0 0 0 1.14-.094l3.75-5.25Z" clip-rule="evenodd" />
        `
    };

    // ============================================
    // Constants
    // ============================================
    const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // ============================================
    // CONTACT FORM - Frontend Validation (UX Layer)
    // Defense in Depth: This is the FIRST layer of validation
    // ============================================
    function initializeContactForm() {
        if (!contactForm) return;
        
        // Add submit event listener for frontend validation
        contactForm.addEventListener('submit', handleContactSubmit);
        
        // Add input listeners to clear errors when user types
        const contactInputs = contactForm.querySelectorAll('input, textarea');
        contactInputs.forEach(input => {
            input.addEventListener('input', function() {
                removeContactErrors(this);
            });
        });
    }
    
    function validateContactForm() {
        const name = contactForm.querySelector('input[name="name"]')?.value.trim();
        const email = contactForm.querySelector('input[name="email"]')?.value.trim();
        const message = contactForm.querySelector('textarea[name="message"]')?.value.trim();
        
        // Name validation
        if (!name || name.length < 2) {
            return {
                isValid: false,
                field: 'name',
                message: 'Name must be at least 2 characters long'
            };
        }
        
        // Email validation
        if (!email) {
            return {
                isValid: false,
                field: 'email',
                message: 'Email is required'
            };
        }
        
        if (!EMAIL_REGEX.test(email)) {
            return {
                isValid: false,
                field: 'email',
                message: 'Please enter a valid email address (example@domain.com)'
            };
        }
        
        // Message validation
        if (!message || message.length < 10) {
            return {
                isValid: false,
                field: 'message',
                message: 'Message must be at least 10 characters long'
            };
        }
        
        return { isValid: true };
    }
    
    function handleContactSubmit(e) {
        // FRONTEND VALIDATION LAYER - For instant user feedback
        const validation = validateContactForm();
        if (!validation.isValid) {
            e.preventDefault(); // Prevent form submission
            showContactError(validation.field, validation.message);
            return;
        }
        
        // If frontend validation passes, show loading state
        // The form will submit normally to backend for SECOND validation layer
        showContactLoading();
        
        // Note: Backend will perform additional security validation
        // and return flash messages for success/error
    }
    
    function showContactError(field, message) {
        // Remove previous errors
        removeContactErrors();
        
        // Create error element
        const errorDiv = document.createElement('div');
        errorDiv.className = 'contact-error';
        errorDiv.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
            </svg>
            <span>${message}</span>
        `;
        
        // Find corresponding field
        const fieldInput = contactForm.querySelector(`[name="${field}"]`);
        if (fieldInput) {
            // Add error class to field
            fieldInput.classList.add('error');
            
            // Insert error message after the field
            fieldInput.parentNode.insertBefore(errorDiv, fieldInput.nextSibling);
            
            // Focus on field with error
            fieldInput.focus();
        } else {
            // If field not found, show at top
            contactForm.insertBefore(errorDiv, contactForm.firstChild);
        }
    }
    
    function removeContactErrors(specificField = null) {
        // Remove all error messages
        const errors = contactForm.querySelectorAll('.contact-error');
        errors.forEach(error => error.remove());
        
        // Remove error class from inputs
        if (specificField) {
            specificField.classList.remove('error');
        } else {
            const allInputs = contactForm.querySelectorAll('input, textarea');
            allInputs.forEach(input => input.classList.remove('error'));
        }
    }
    
    function showContactLoading() {
        const submitButton = contactForm.querySelector('.cta-button.cta-send');
        if (!submitButton) return;
        
        // Save original text
        if (!submitButton.dataset.originalText) {
            submitButton.dataset.originalText = submitButton.innerHTML;
        }
        
        // Show loading state
        submitButton.disabled = true;
        submitButton.innerHTML = `
            <span class="loading-spinner">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="spinner-circle" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="spinner-path" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
            </span>
            Sending...
        `;
    }

        document.addEventListener('DOMContentLoaded', function() {
        // Se a URL tem âncora #contact, rola até ela
        if (window.location.hash === '#contact') {
            setTimeout(() => {
                const contactSection = document.getElementById('contact');
                if (contactSection) {
                    contactSection.scrollIntoView({ behavior: 'smooth' });
                }
            }, 100);
        }
    });

    // ============================================
    // LOGIN FORM - Frontend Validation
    // ============================================
    function initializePasswordToggle() {
        if (!togglePassword || !passwordInput || !eyeIcon) return;
        
        togglePassword.addEventListener('click', function() {
            const isPassword = passwordInput.getAttribute('type') === 'password';
            const newType = isPassword ? 'text' : 'password';
            
            // Toggle input type
            passwordInput.setAttribute('type', newType);
            
            // Update icon
            eyeIcon.innerHTML = isPassword ? svgIcons.eyeClosed : svgIcons.eyeOpen;
        });
    }

    function validateEmail(email) {
        if (!email) {
            return { isValid: false, message: 'Please fill in all fields.' };
        }
        
        if (!EMAIL_REGEX.test(email)) {
            return { isValid: false, message: 'Please enter a valid email address.' };
        }
        
        return { isValid: true };
    }

    function validatePassword(password) {
        if (!password) {
            return { isValid: false, message: 'Please fill in all fields.' };
        }
        
        return { isValid: true };
    }

    function validateForm(email, password) {
        const emailValidation = validateEmail(email);
        if (!emailValidation.isValid) {
            return emailValidation;
        }
        
        const passwordValidation = validatePassword(password);
        if (!passwordValidation.isValid) {
            return passwordValidation;
        }
        
        return { isValid: true };
    }

    function showLoadingState() {
        if (!loginButton) return;
        
        loginButton.disabled = true;
        loginButton.innerHTML = `
            <span class="auth-loading-spinner">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="spinner-circle" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="spinner-path" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
            </span>
            Signing in...
        `;
    }

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
        
        // Insert error message
        const formHeader = document.querySelector('.auth-card-header');
        if (formHeader) {
            formHeader.parentNode.insertBefore(errorDiv, formHeader.nextElementSibling);
        }
        
        // Scroll to error for better UX
        errorDiv.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
    }

    function removeExistingErrors() {
        const existingErrors = document.querySelectorAll('.auth-message.error');
        existingErrors.forEach(error => error.remove());
    }

    function handleFormSubmit(e) {
        e.preventDefault();
        
        // Get form values
        const email = document.getElementById('email')?.value.trim();
        const password = document.getElementById('password')?.value;
        
        // Validate form
        const validation = validateForm(email, password);
        if (!validation.isValid) {
            showError(validation.message);
            return;
        }
        
        // Show loading state
        showLoadingState();
        
        // IMPORTANT: For production, remove simulation and let form submit
        // Currently this prevents actual submission - adjust based on backend setup
        
        // For now, simulate submission (remove in production)
        setTimeout(() => {
            // In production: Allow form to submit to backend
            // loginForm.submit(); // Uncomment for actual submission
            
            // Reset button for demo purposes
            loginButton.disabled = false;
            loginButton.textContent = 'Sign In';
        }, 1000);
    }

    // ============================================
    // Accessibility Enhancements
    // ============================================
    function enhanceAccessibility() {
        // Add ARIA labels to password toggle
        if (togglePassword) {
            togglePassword.setAttribute('aria-label', 'Toggle password visibility');
            togglePassword.setAttribute('aria-pressed', 'false');
            
            // Update aria-pressed when toggling
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
    // Input Event Listeners
    // ============================================
    function setupInputValidation() {
        const emailInput = document.getElementById('email');
        const passwordInput = document.getElementById('password');
        
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
        // Initialize password toggle
        initializePasswordToggle();
        
        // Initialize contact form validation (FRONTEND LAYER)
        initializeContactForm();
        
        // Setup login form submission
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
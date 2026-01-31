document.addEventListener('DOMContentLoaded', function() {
    // ============================================
    // DOM Elements 
    // ============================================
    
    // Contact Form Elements
    const contactForm = document.getElementById('contactForm');
    const contactSubmitButton = contactForm?.querySelector('.cta-button.cta-send');
    
    // Carousel Elements
    const parksCarousel = document.querySelector('.parks-carousel');
    const carouselPrevBtn = document.querySelector('.carousel-arrow-left');
    const carouselNextBtn = document.querySelector('.carousel-arrow-right');
    
    // Park Gallery Elements
    const galleryMainImg = document.getElementById('gallery-main-img');
    const galleryThumbItems = document.querySelectorAll('.thumb-item');
    const galleryPrevBtn = document.querySelector('.prev-btn');
    const galleryNextBtn = document.querySelector('.next-btn');
    
    // Booking Form Elements
    const bookingForm = document.getElementById('bookingForm');
    const healthLink = document.getElementById('health-link');
    const backLink = document.getElementById('backToProfile');
    const healthCheckbox = document.getElementById('health_safety');
    const returnBtn = document.getElementById('returnToBooking');
    const dateInput = document.querySelector('input[type="date"]');
    const parkSelect = document.getElementById('parkSelect');
    const visitDate = document.getElementById('visitDate');
    const numTickets = document.getElementById('numTickets');
    
    // ============================================
    // SVG Icons Configuration
    // ============================================
    const svgIcons = {
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
    const TOTAL_GALLERY_IMAGES = 4;

    // ============================================
    // Contact Form Functions
    // Defense in Depth: This is the FIRST layer of validation
    // ============================================
    
    function validateContactForm() {
        if (!contactForm) return { isValid: true };
        
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
        if (!contactForm) return;
        
        // FRONTEND VALIDATION LAYER - For instant user feedback
        const validation = validateContactForm();
        if (!validation.isValid) {
            e.preventDefault();
            showContactError(validation.field, validation.message);
            return;
        }
        
        // If frontend validation passes, show loading state
        // The form will submit normally to backend for SECOND validation layer
        showContactLoading();
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
        if (!contactForm) return;
        
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
        if (!contactSubmitButton) return;
        
        // Save original text
        if (!contactSubmitButton.dataset.originalText) {
            contactSubmitButton.dataset.originalText = contactSubmitButton.innerHTML;
        }
        
        // Show loading state
        contactSubmitButton.disabled = true;
        contactSubmitButton.innerHTML = `
            <span class="loading-spinner">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle class="spinner-circle" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="spinner-path" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
            </span>
            Sending...
        `;
    }

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

    // ============================================
    // Carousel Functions
    // ============================================
    
    function initializeCarousel() {
        if (!parksCarousel || !carouselPrevBtn || !carouselNextBtn) return;
        
        // Disable left button initially
        carouselPrevBtn.disabled = true;
        
        function updateCarouselButtons() {
            const isAtStart = parksCarousel.scrollLeft <= 10;
            const isAtEnd = parksCarousel.scrollLeft + parksCarousel.clientWidth >= parksCarousel.scrollWidth - 10;
            
            carouselPrevBtn.disabled = isAtStart;
            carouselNextBtn.disabled = isAtEnd;
        }
        
        // Click events
        carouselPrevBtn.addEventListener('click', () => {
            if (!carouselPrevBtn.disabled) {
                parksCarousel.scrollBy({ left: -300, behavior: 'smooth' });
            }
        });
        
        carouselNextBtn.addEventListener('click', () => {
            if (!carouselNextBtn.disabled) {
                parksCarousel.scrollBy({ left: 300, behavior: 'smooth' });
            }
        });
        
        // Scroll and resize events
        parksCarousel.addEventListener('scroll', updateCarouselButtons);
        window.addEventListener('resize', updateCarouselButtons);
        
        // Initial updates
        setTimeout(updateCarouselButtons, 100);
        setTimeout(updateCarouselButtons, 500);
        window.addEventListener('load', updateCarouselButtons);
    }

    // ============================================
    // Park Gallery Functions
    // ============================================
    
    function initializeGallery() {
        if (!galleryMainImg || galleryThumbItems.length === 0) return;
        
        let currentGalleryIndex = 1;
        
        function updateMainImage(index) {
            const thumb = document.querySelector(`.thumb-item[data-index="${index}"]`);
            if (!thumb) return;
            
            galleryMainImg.src = thumb.dataset.src;
            
            galleryThumbItems.forEach(item => {
                item.classList.remove('active');
            });
            thumb.classList.add('active');
            
            if (galleryPrevBtn) galleryPrevBtn.disabled = index === 1;
            if (galleryNextBtn) galleryNextBtn.disabled = index === TOTAL_GALLERY_IMAGES;
            
            currentGalleryIndex = index;
        }
        
        // Events for thumbnails
        galleryThumbItems.forEach(thumb => {
            thumb.addEventListener('click', function() {
                const index = parseInt(this.dataset.index);
                updateMainImage(index);
            });
        });
        
        // Navigation with buttons
        if (galleryPrevBtn) {
            galleryPrevBtn.addEventListener('click', function() {
                if (currentGalleryIndex > 1) updateMainImage(currentGalleryIndex - 1);
            });
        }
        
        if (galleryNextBtn) {
            galleryNextBtn.addEventListener('click', function() {
                if (currentGalleryIndex < TOTAL_GALLERY_IMAGES) updateMainImage(currentGalleryIndex + 1);
            });
        }
        
        // Keyboard navigation
        document.addEventListener('keydown', function(e) {
            if (e.key === 'ArrowLeft' && galleryPrevBtn) galleryPrevBtn.click();
            if (e.key === 'ArrowRight' && galleryNextBtn) galleryNextBtn.click();
        });
        
        // Initialization
        updateMainImage(1);
    }

    // ============================================
    // Booking Form Functions
    // ============================================
    
    function initializeBookingForm() {
        // Set min date to today for date inputs
        if (dateInput) {
            const today = new Date().toISOString().split('T')[0];
            dateInput.min = today;
            
            // If no value is set, default to today
            if (!dateInput.value) {
                dateInput.value = today;
            }
        }
        
        // Save form data before navigating to Health & Safety Guidelines
        if (healthLink) {
            healthLink.addEventListener('click', function(e) {
                const formData = {
                    park_id: parkSelect?.value || '',
                    date: visitDate?.value || '',
                    num_tickets: numTickets?.value || ''
                };
                
                sessionStorage.setItem('bookingFormData', JSON.stringify(formData));
            });
        }
        
        // Restore saved form data
        const savedData = sessionStorage.getItem('bookingFormData');
        if (savedData) {
            try {
                const formData = JSON.parse(savedData);
                
                if (formData.park_id && parkSelect) {
                    parkSelect.value = formData.park_id;
                }
                
                if (formData.date && visitDate) {
                    visitDate.value = formData.date;
                }
                
                if (formData.num_tickets && numTickets) {
                    numTickets.value = formData.num_tickets;
                }
            } catch (e) {
                console.error('Error parsing saved form data:', e);
            }
        }
        
        // Handle health safety checkbox state
        if (healthCheckbox) {
            healthCheckbox.disabled = true;
            
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('health_safety_read') === 'true') {
                healthCheckbox.disabled = false;
                healthCheckbox.checked = true;
                
                // Clean URL
                const newUrl = window.location.pathname;
                window.history.replaceState({}, '', newUrl);
            }
        }
        
        // Form submission handling
        if (bookingForm) {
            bookingForm.addEventListener('submit', function() {
                sessionStorage.removeItem('bookingFormData');
            });
            
            // Validate checkbox on submit
            bookingForm.addEventListener('submit', function(e) {
                if (healthCheckbox && !healthCheckbox.checked) {
                    e.preventDefault();
                    alert('You must acknowledge and agree to the health & safety guidelines.');
                    if (healthLink) {
                        healthLink.scrollIntoView({ behavior: 'smooth' });
                    }
                    return false;
                }
            });
        }
        
        // Back link handling
        if (backLink) {
            backLink.addEventListener('click', function() {
                sessionStorage.removeItem('bookingFormData');
            });
        }
        
        // Return to Booking button
        if (returnBtn) {
            localStorage.setItem('healthSafetyRead', 'true');
        }
    }

    // ============================================
    // Page Navigation Utilities
    // ============================================
    
    function initializePageNavigation() {
        // Scroll to contact section if URL has #contact anchor
        if (window.location.hash === '#contact') {
            setTimeout(() => {
                const contactSection = document.getElementById('contact');
                if (contactSection) {
                    contactSection.scrollIntoView({ behavior: 'smooth' });
                }
            }, 100);
        }
    }

    // ============================================
    // UI State Management
    // ============================================
    
    // (Reserved for shared UI state functions if needed in future)

    // ============================================
    // Initialization
    // ============================================
    
    function initialize() {
        // Initialize contact form validation
        initializeContactForm();
        
        // Initialize parks carousel
        initializeCarousel();
        
        // Initialize park gallery
        initializeGallery();
        
        // Initialize booking form
        initializeBookingForm();
        
        // Initialize page navigation utilities
        initializePageNavigation();
    }

    // ============================================
    // Start Application
    // ============================================
    
    initialize();
});
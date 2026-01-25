document.addEventListener('DOMContentLoaded', function() {
  const carousel = document.querySelector('.parks-carousel');
  const prevBtn = document.querySelector('.carousel-arrow-left');
  const nextBtn = document.querySelector('.carousel-arrow-right');
  
  if (!carousel || !prevBtn || !nextBtn) return;
  
  // Desabilita o botão esquerda
  prevBtn.disabled = true;
  
  // Atualizar estado dos botões
  function updateButtons() {
    const isAtStart = carousel.scrollLeft <= 10;
    const isAtEnd = carousel.scrollLeft + carousel.clientWidth >= carousel.scrollWidth - 10;
    
    prevBtn.disabled = isAtStart;
    nextBtn.disabled = isAtEnd;
  }
  
  // Click events
  prevBtn.addEventListener('click', () => {
    if (!prevBtn.disabled) {
      carousel.scrollBy({ left: -300, behavior: 'smooth' });
    }
  });
  
  nextBtn.addEventListener('click', () => {
    if (!nextBtn.disabled) {
      carousel.scrollBy({ left: 300, behavior: 'smooth' });
    }
  });
  
  // Events de scroll e resize
  carousel.addEventListener('scroll', updateButtons);
  window.addEventListener('resize', updateButtons);
  
  // Inicital events
  setTimeout(updateButtons, 100);
  setTimeout(updateButtons, 500);

  window.addEventListener('load', updateButtons);
  
});

/* ============================
Park Gallery Functionality 
=============================*/

document.addEventListener('DOMContentLoaded', function() {
  const mainImg = document.getElementById('gallery-main-img');
  const thumbItems = document.querySelectorAll('.thumb-item');
  const prevBtn = document.querySelector('.prev-btn');
  const nextBtn = document.querySelector('.next-btn');
  
  let currentIndex = 1;
  const totalImages = 4;
  
  // Atualiza imagem principal
  function updateMainImage(index) {
    const thumb = document.querySelector(`.thumb-item[data-index="${index}"]`);
    if (!thumb) return;
    
    mainImg.src = thumb.dataset.src;
    
    thumbItems.forEach(item => {
      item.classList.remove('active');
    });
    thumb.classList.add('active');
    
    prevBtn.disabled = index === 1;
    nextBtn.disabled = index === totalImages;
    
    currentIndex = index;
  }
  
  // Eventos para thumbnails
  thumbItems.forEach(thumb => {
    thumb.addEventListener('click', function() {
      const index = parseInt(this.dataset.index);
      updateMainImage(index);
    });
  });
  
  // Navegação com botões
  prevBtn.addEventListener('click', function() {
    if (currentIndex > 1) updateMainImage(currentIndex - 1);
  });
  
  nextBtn.addEventListener('click', function() {
    if (currentIndex < totalImages) updateMainImage(currentIndex + 1);
  });
  
  // Navegação com teclado
  document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowLeft') prevBtn.click();
    if (e.key === 'ArrowRight') nextBtn.click();
  });
  
  // Inicialização
  updateMainImage(1);
});


/* ============================
Booking Form Validation 
=============================*/
    // Set min date to today
  document.addEventListener('DOMContentLoaded', function() {
    const today = new Date().toISOString().split('T')[0];
    const dateInput = document.querySelector('input[type="date"]');
     dateInput.min = today;
    
    // If no value is set, default to today
    if (!dateInput.value) {
        dateInput.value = today;
        }
    });

/* ============================
Checkbox Handling 
=============================*/
/* Save Form Data Before Navigating to Health & Safety Guidelines */

    document.addEventListener('DOMContentLoaded', function() {
        const form = document.getElementById('bookingForm');
        const healthLink = document.getElementById('health-link');
        const backLink = document.getElementById('backToProfile');
        const checkbox = document.getElementById('health_safety');
    
    if (checkbox) {
        checkbox.disabled = true;
    }
    
    if (healthLink) {
        healthLink.addEventListener('click', function(e) {
            const formData = {
                park_id: document.getElementById('parkSelect').value,
                date: document.getElementById('visitDate').value,
                num_tickets: document.getElementById('numTickets').value
            };
            
            sessionStorage.setItem('bookingFormData', JSON.stringify(formData));
        });
    }
    
    const savedData = sessionStorage.getItem('bookingFormData');
    if (savedData) {
        try {
            const formData = JSON.parse(savedData);
            
            if (formData.park_id) {
                const parkSelect = document.getElementById('parkSelect');
                if (parkSelect) {
                    parkSelect.value = formData.park_id;
                }
            }
            
            if (formData.date) {
                const visitDate = document.getElementById('visitDate');
                if (visitDate) {
                    visitDate.value = formData.date;
                }
            }
            
            if (formData.num_tickets) {
                const numTickets = document.getElementById('numTickets');
                if (numTickets) {
                    numTickets.value = formData.num_tickets;
                }
            }
        } catch (e) {
            console.error('Error parsing saved form data:', e);
        }
    }
    
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('health_safety_read') === 'true') {
        if (checkbox) {
            checkbox.disabled = false;
            checkbox.checked = true;
        }
        
        const newUrl = window.location.pathname;
        window.history.replaceState({}, '', newUrl);
    }
    
    if (form) {
        form.addEventListener('submit', function() {
            sessionStorage.removeItem('bookingFormData');
        });
    }
    
    if (backLink) {
        backLink.addEventListener('click', function() {
            sessionStorage.removeItem('bookingFormData');
        });
    }
    
    if (form) {
        form.addEventListener('submit', function(e) {
            if (checkbox && !checkbox.checked) {
                e.preventDefault();
                alert('You must acknowledge and agree to the health & safety guidelines.');
                healthLink.scrollIntoView({ behavior: 'smooth' });
                return false;
            }
        });
    }
});

/* Return to Booking Button */
document.addEventListener('DOMContentLoaded', function() {
    const returnBtn = document.getElementById('returnToBooking');
    if (returnBtn) {
        localStorage.setItem('healthSafetyRead', 'true');
    }
});
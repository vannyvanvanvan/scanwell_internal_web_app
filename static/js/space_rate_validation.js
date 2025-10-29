// Frontend validation Sugrate must be >= Avgrate

document.addEventListener('DOMContentLoaded', function() {
    const avgrateInput = document.getElementById('avgrate');
    const sugrateInput = document.getElementById('sugrate');
    const form = document.querySelector('form');
    
    if (!avgrateInput || !sugrateInput || !form) {
        return;
    }
    
    function validateRates() {
        const avgrate = parseInt(avgrateInput.value) || 0;
        const sugrate = parseInt(sugrateInput.value) || 0;
        const submitButton = form.querySelector('input[type="submit"]');
        
        // Remove previous error styling
        avgrateInput.classList.remove('is-invalid', 'schedule-validation-error');
        sugrateInput.classList.remove('is-invalid', 'schedule-validation-error');
        
        // Remove previous error messages
        let errorDiv = avgrateInput.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) errorDiv.remove();
        errorDiv = sugrateInput.parentNode.querySelector('.invalid-feedback');
        if (errorDiv) errorDiv.remove();
        
        // Only validate if both fields have values
        if (avgrateInput.value && sugrateInput.value && sugrate < avgrate) {
            // Add error styling
            avgrateInput.classList.add('is-invalid', 'schedule-validation-error');
            sugrateInput.classList.add('is-invalid', 'schedule-validation-error');
            
            // Add error message to sugrate field
            errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback';
            errorDiv.textContent = 'Sugrate must be greater than or equal to Avgrate.';
            sugrateInput.parentNode.appendChild(errorDiv);
            
            // Disable submit button
            if (submitButton) {
                submitButton.disabled = true;
                submitButton.classList.add('btn-secondary');
                submitButton.classList.remove('btn-primary');
                submitButton.title = 'Sugrate must be >= Avgrate';
            }
            
            return false;
        } else {
            // Enable submit button
            if (submitButton) {
                submitButton.disabled = false;
                submitButton.classList.add('btn-primary');
                submitButton.classList.remove('btn-secondary');
                submitButton.title = '';
            }
            return true;
        }
    }
    
    // Validate on input changes
    avgrateInput.addEventListener('input', validateRates);
    avgrateInput.addEventListener('blur', validateRates);
    sugrateInput.addEventListener('input', validateRates);
    sugrateInput.addEventListener('blur', validateRates);
    
    // Validate on form submit
    form.addEventListener('submit', function(e) {
        if (!validateRates()) {
            e.preventDefault();
            return false;
        }
    });
    
    // Initial validation
    validateRates();
});


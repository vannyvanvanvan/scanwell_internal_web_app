 // Shipping Schedules Validation

class ScheduleDateValidator {
    constructor() {
        this.dateFields = {
            cyopen: 'cyopen',
            sicutoff: 'sicutoff',
            sicutoffTime: 'sicutoff_time',
            cycvcls: 'cycvcls',
            cycvclsTime: 'cycvcls_time',
            etd: 'etd',
            eta: 'eta'
        };
        
        // Error messages
        this.errorMessages = {
            etaBeforeEtd: 'ETA must be greater than or equal to ETD',
            etdBeforeCycvcls: 'ETD must be greater than CY CV CLOSING',
            cycvclsBeforeSicutoff: 'CY CV CLOSING must be greater than or equal to SI CUTOFF',
            sicutoffBeforeCyopen: 'SI CUTOFF must be greater than CY OPEN'
        };
        
        this.init();
    }
    
    init() {
        Object.values(this.dateFields).forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('change', () => this.validateAll());
                field.addEventListener('blur', () => this.validateAll());
            }
        });
        
        // Validate on form submit
        const form = document.querySelector('form');
        if (form) {
            form.addEventListener('submit', (e) => {
                if (!this.validateAll()) {
                    e.preventDefault();
                    return false;
                }
            });
        }
        this.validateAll();
    }
    
    parseDate(dateStr) {
        if (!dateStr) return null;
        return new Date(dateStr);
    }
    
    parseDateTime(dateStr, timeStr) {
        if (!dateStr || !timeStr) return null;
        return new Date(`${dateStr}T${timeStr}`);
    }
    
    validateAll() {
        const cyopen = this.parseDate(document.getElementById(this.dateFields.cyopen)?.value);
        const sicutoff = this.parseDateTime(
            document.getElementById(this.dateFields.sicutoff)?.value,
            document.getElementById(this.dateFields.sicutoffTime)?.value
        );
        const cycvcls = this.parseDateTime(
            document.getElementById(this.dateFields.cycvcls)?.value,
            document.getElementById(this.dateFields.cycvclsTime)?.value
        );
        const etd = this.parseDate(document.getElementById(this.dateFields.etd)?.value);
        const eta = this.parseDate(document.getElementById(this.dateFields.eta)?.value);
        this.clearAllErrors();
        
        let isValid = true;
        let errorMessage = '';
        
        // ETA >= ETD > CY CV CLOSING >= SI CUTOFF > CY OPEN
        if (eta && etd && eta < etd) {
            this.showError('eta', this.errorMessages.etaBeforeEtd);
            this.showError('etd', this.errorMessages.etaBeforeEtd);
            isValid = false;
            errorMessage = this.errorMessages.etaBeforeEtd;
        }
        
        if (etd && cycvcls && etd <= cycvcls) {
            this.showError('etd', this.errorMessages.etdBeforeCycvcls);
            this.showError('cycvcls', this.errorMessages.etdBeforeCycvcls);
            isValid = false;
            errorMessage = this.errorMessages.etdBeforeCycvcls;
        }
        
        if (cycvcls && sicutoff && cycvcls < sicutoff) {
            this.showError('cycvcls', this.errorMessages.cycvclsBeforeSicutoff);
            this.showError('sicutoff', this.errorMessages.cycvclsBeforeSicutoff);
            isValid = false;
            errorMessage = this.errorMessages.cycvclsBeforeSicutoff;
        }
        
        if (sicutoff && cyopen) {
            // Convert cyopen to end of day for proper comparison
            const cyopenEndOfDay = new Date(cyopen);
            cyopenEndOfDay.setHours(23, 59, 59, 999);
            
            if (sicutoff <= cyopenEndOfDay) {
                this.showError('sicutoff', this.errorMessages.sicutoffBeforeCyopen);
                this.showError('cyopen', this.errorMessages.sicutoffBeforeCyopen);
                isValid = false;
                errorMessage = this.errorMessages.sicutoffBeforeCyopen;
            }
        }
        
        // Update submit button state
        this.updateSubmitButton(isValid, errorMessage);
        
        return isValid;
    }
    
    showError(fieldId, message) {
        const field = document.getElementById(fieldId);
        if (!field) return;
        field.classList.add('is-invalid');
        // Create or update error message
        let errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback';
            field.parentNode.appendChild(errorDiv);
        }
        errorDiv.textContent = message;
    }
    
    clearAllErrors() {
        Object.values(this.dateFields).forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.classList.remove('is-invalid');
                const errorDiv = field.parentNode.querySelector('.invalid-feedback');
                if (errorDiv) {
                    errorDiv.remove();
                }
            }
        });
    }
    
    updateSubmitButton(isValid, errorMessage) {
        const submitBtn = document.querySelector('input[type="submit"]');
        if (!submitBtn) return;
        
        if (!isValid) {
            submitBtn.disabled = true;
            submitBtn.title = `Date sequence error: ${errorMessage}`;
            submitBtn.classList.add('btn-secondary');
            submitBtn.classList.remove('btn-primary');
        } else {
            submitBtn.disabled = false;
            submitBtn.title = '';
            submitBtn.classList.add('btn-primary');
            submitBtn.classList.remove('btn-secondary');
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    new ScheduleDateValidator();
});

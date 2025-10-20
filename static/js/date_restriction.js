// Schedule Date Restriction

class DateRestriction {
    constructor() {
        this.dateFields = {
            cyopen: 'cyopen',
            sicutoff: 'sicutoff',
            cycvcls: 'cycvcls',
            etd: 'etd',
            eta: 'eta'
        };
        this.init();
    }

    init() {
        Object.values(this.dateFields).forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('change', () => this.updateAllRestrictions());
            }
        });
        this.updateAllRestrictions();
    }

    getFieldValue(fieldId) {
        const field = document.getElementById(fieldId);
        return field ? field.value : null;
    }

    setMinDate(fieldId, minDate) {
        const field = document.getElementById(fieldId);
        if (field && minDate) {
            field.setAttribute('min', minDate);
        }
    }

    setMaxDate(fieldId, maxDate) {
        const field = document.getElementById(fieldId);
        if (field && maxDate) {
            field.setAttribute('max', maxDate);
        }
    }

    clearRestrictions(fieldId) {
        const field = document.getElementById(fieldId);
        if (field) {
            field.removeAttribute('min');
            field.removeAttribute('max');
        }
    }

    addDays(dateStr, days) {
        if (!dateStr) return null;
        const date = new Date(dateStr);
        date.setDate(date.getDate() + days);
        return date.toISOString().split('T')[0];
    }

    updateAllRestrictions() {
        const cyopen = this.getFieldValue(this.dateFields.cyopen);
        const sicutoff = this.getFieldValue(this.dateFields.sicutoff);
        const cycvcls = this.getFieldValue(this.dateFields.cycvcls);
        const etd = this.getFieldValue(this.dateFields.etd);
        const eta = this.getFieldValue(this.dateFields.eta);

        // CY OPEN restrictions
        this.clearRestrictions(this.dateFields.cyopen);
        if (sicutoff) {
            this.setMaxDate(this.dateFields.cyopen, this.addDays(sicutoff, -1));
        }

        // SI CUTOFF restrictions
        this.clearRestrictions(this.dateFields.sicutoff);
        if (cyopen) {
            this.setMinDate(this.dateFields.sicutoff, this.addDays(cyopen, 1));
        }
        if (cycvcls) {
            this.setMaxDate(this.dateFields.sicutoff, cycvcls);
        }

        // CY CV CLOSING restrictions
        this.clearRestrictions(this.dateFields.cycvcls);
        if (sicutoff) {
            this.setMinDate(this.dateFields.cycvcls, sicutoff);
        }
        if (etd) {
            this.setMaxDate(this.dateFields.cycvcls, this.addDays(etd, -1));
        }

        // ETD restrictions
        this.clearRestrictions(this.dateFields.etd);
        if (cycvcls) {
            this.setMinDate(this.dateFields.etd, this.addDays(cycvcls, 1));
        }
        if (eta) {
            this.setMaxDate(this.dateFields.etd, eta);
        }

        // ETA restrictions
        this.clearRestrictions(this.dateFields.eta);
        if (etd) {
            this.setMinDate(this.dateFields.eta, etd);
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    new DateRestriction();
});


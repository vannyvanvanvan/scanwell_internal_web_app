// Handle void checkbox and space status selection for confirmed bookings

document.addEventListener('DOMContentLoaded', function() {
    const voidCheckbox = document.getElementById('void');
    
    if (voidCheckbox) {
        voidCheckbox.addEventListener('change', function() {
            const statusDiv = document.getElementById('void_space_status_div');
            const currentStatus = document.getElementById('current_space_status');
            
            if (this.checked) {
                statusDiv.style.display = 'flex';
                currentStatus.classList.remove('status-disabled');
                currentStatus.classList.add('status-warning');
            } else {
                statusDiv.style.display = 'none';
                currentStatus.classList.remove('status-warning');
                currentStatus.classList.add('status-disabled');
            }
        });
    }
});


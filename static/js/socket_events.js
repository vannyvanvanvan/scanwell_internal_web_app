var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

// Function to update the user status
function updateStatus(status) {
    socket.emit("user_status", { status: status });
}

// Marking user as online on page load
window.onload = function () { updateStatus('online'); };
window.onfocus = function () { updateStatus('online'); };
window.onblur = function () { updateStatus('away'); };
window.onbeforeunload = function () { updateStatus('offline'); };

// Detect AFK (10 minutes)
let afkTimer;

function resetTimer() {
    clearTimeout(afkTimer);
    // Ensure user is marked active on any movement
    updateStatus('online'); 

    // Set a timer to mark them as away after 10 minutes of inactivity
    afkTimer = setTimeout(() => { 
        updateStatus("away");
    }, 600000);
}

// Listen for user activity to prevent AFK
document.addEventListener("mousemove", resetTimer);
document.addEventListener("keypress", resetTimer);
document.addEventListener("mousedown", resetTimer);
document.addEventListener("touchstart", resetTimer);
document.addEventListener("scroll", resetTimer);

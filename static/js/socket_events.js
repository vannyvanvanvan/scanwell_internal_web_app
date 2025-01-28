var socket = io.connect(window.location.protocol + "//" + document.domain + ":" + location.port);

var awayTimeout = setTimeout(setUserAway, 180000);
var isAway = false;  

function resetTimer() {
    clearTimeout(awayTimeout);
    if (isAway) {  
        // Only emit if the user was previously away
        socket.emit("user_active");  
        isAway = false;
    }
    awayTimeout = setTimeout(setUserAway, 180000);
}

function setUserAway() {
    // Only emit if the user was previously active
    if (!isAway) {  
        console.log("[DEBUG] User is idle.");
        socket.emit("user_away");
        isAway = true;
    }
}

// Detect user interaction
window.onload = resetTimer;
document.onmousemove = resetTimer;
document.onkeypress = resetTimer;
document.onclick = resetTimer;
document.onscroll = resetTimer;

// Listen for WebSocket events
socket.on("connect", function () {
    console.log("[DEBUG] Connected to WebSocket");
    // Mark user as active on connection
    socket.emit("user_active"); 
    isAway = false;
});

socket.on("disconnect", function () {
    console.log("[DEBUG] Disconnected from WebSocket");
});

socket.on("update_online_status", function (data) {
    console.log("[DEBUG] User status updated:", data.status);
});

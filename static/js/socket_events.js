var socket = io.connect(window.location.protocol + "//" + document.domain + ":" + location.port);

// Detect idle user and mark as away after 3 minutes
var awayTimeout = setTimeout(setUserAway, 180000);

function resetTimer() {
    clearTimeout(awayTimeout);
    socket.emit("user_active");
    awayTimeout = setTimeout(setUserAway, 180000);
}

function setUserAway() {
    console.log("User is idle.");
    socket.emit("user_away");
}

// Detect user interaction
window.onload = resetTimer;
document.onmousemove = resetTimer;
document.onkeypress = resetTimer;
document.onclick = resetTimer;
document.onscroll = resetTimer;

// Listen for updates
socket.on("update_online_status", function (data) {
    console.log("User status updated:", data.status);
});


socket.on("connect", function () {
    console.log("[DEBUG] Connected to WebSocket");
    socket.emit("user_active");
});

socket.on("disconnect", function () {
    console.log("[DEBUG] Disconnected from WebSocket");
});

function controlServo(direction) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/control", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("direction=" + direction);
}

// Add event listeners
// UP
document.getElementById("up").addEventListener("mousedown", function() {
    controlServo("up");
});
document.getElementById("up").addEventListener("touchstart", function() {
    controlServo("up");
});
document.getElementById("up").addEventListener("mouseup", function() {
    controlServo("stop");
});
document.getElementById("up").addEventListener("touchend", function() {
    controlServo("stop");
});

// DOWN
document.getElementById("down").addEventListener("mousedown", function() {
    controlServo("down");
});
document.getElementById("down").addEventListener("touchstart", function() {
    controlServo("down");
});
document.getElementById("down").addEventListener("mouseup", function() {
    controlServo("stop");
});
document.getElementById("down").addEventListener("touchend", function() {
    controlServo("stop");
});

// LEFT
document.getElementById("left").addEventListener("mousedown", function() {
    controlServo("left");
});
document.getElementById("left").addEventListener("touchstart", function() {
    controlServo("left");
});
document.getElementById("left").addEventListener("mouseup", function() {
    controlServo("stop");
});
document.getElementById("left").addEventListener("touchend", function() {
    controlServo("stop");
});

// RIGHT
document.getElementById("right").addEventListener("mousedown", function() {
    controlServo("right");
});
document.getElementById("right").addEventListener("touchstart", function() {
    controlServo("right");
});
document.getElementById("right").addEventListener("mouseup", function() {
    controlServo("stop");
});
document.getElementById("right").addEventListener("touchend", function() {
    controlServo("stop");
});

// STOP
document.getElementById("stop").addEventListener("mousedown", function() {
    controlServo("stop");
});
document.getElementById("stop").addEventListener("touchstart", function() {
    controlServo("stop");
});
document.getElementById("stop").addEventListener("mouseup", function() {
    controlServo("stop");
});
document.getElementById("stop").addEventListener("touchend", function() {
    controlServo("stop");
});



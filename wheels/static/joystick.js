var joystickIsActive = false;  // This variable tracks whether the joystick is active

var joystick1 = nipplejs.create({
    zone: document.getElementById('joystick-1'),
    mode: 'static',
    position: { left: '50%', top: '50%' },
    color: 'black',
    size: 200  // Adjust size to fit within the container
});

var lastAngle = 'stop';  // Track the last sent angle
var lastForce = 0;       // Track the last sent force
var inactivityTimeout;   // Variable to store the timeout for inactivity

// When the joystick is moved
joystick1.on('move', function (evt, data) {
    clearTimeout(inactivityTimeout);  // Clear any existing timeout
    joystickIsActive = true;  // Set to true when the joystick is being moved

    if (data.direction) {
        var currentAngle = data.angle.degree;
        var currentForce = data.distance / 100; // Adjusted normalization factor for smaller joystick
        if (currentForce > 1) currentForce = 1;

        if (currentAngle !== lastAngle || currentForce !== lastForce) {
            lastAngle = currentAngle;
            lastForce = currentForce;
            console.log('Joystick 1 - Angle: ' + currentAngle + ', Force: ' + currentForce);
            controlCar(currentAngle, currentForce);
        }
    }
});

// When the joystick is released
joystick1.on('end', function () {
    joystickIsActive = false;  // Set to false when the joystick is released
    inactivityTimeout = setTimeout(function () {
        if (lastAngle !== 'stop' || lastForce !== 0) {
            lastAngle = 'stop';
            lastForce = 0;
            console.log('Joystick 1 released, sending stop command');
            controlCar('stop', 0);
        }
    }, 0); 
});

// Function to send the control command to the server
function controlCar(angle, force) {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/control", true);
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.send("angle=" + angle + "&force=" + force);
}

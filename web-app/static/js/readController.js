const refreshRate = 20;
setInterval(pollController, refreshRate);
var socket = io();
socket.on()

let sentZero = false;
const output = document.getElementById('controller');

function pollController() {
    const [gp] = navigator.getGamepads();

    let x1 = 0;
    let y1 = 0;
    let x2 = 0;
    let y2 = 0;
    x1 += filterDeadzone(Math.round(gp.axes[0] * 100) / 100); // Left JST X
    y1 -= filterDeadzone(Math.round(gp.axes[1] * 100) / 100); // Left JST Y (inverted)
    x2 += filterDeadzone(Math.round(gp.axes[2] * 100) / 100); // Right JST X
    y2 -= filterDeadzone(Math.round(gp.axes[3] * 100) / 100); // Right JST Y (inverted)

    // if any of the values are not 0, send them to the server
    if (x1 != 0.00 || y1 != 0.00 || x2 != 0.00 || y2 != 0.00) {
        socket.emit('controller', {x1, y1, x2, y2});
        output.innerHTML = `Right joystick: (${x2} \t${y2}) `;
        sentZero = false;
    } else if (!sentZero) {
        socket.emit('controller', {x1, y1, x2, y2});
        output.innerHTML = `Right joystick: (${x2} \t${y2}) `;
        sentZero = true;
    }
}

function filterDeadzone(value) {
    const deadzone = 0.05;
    return (Math.abs(value) > deadzone) ? value : 0;
}

//requestAnimationFrame(pollController);

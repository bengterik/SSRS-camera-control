const refreshRate = 100;
setInterval(pollController, refreshRate);

function pollController() {
    const [gp] = navigator.getGamepads();
    const output = document.getElementById('output');
    
    let x1 = 0;
    let y1 = 0;
    let x2 = 0;
    let y2 = 0;
    x1 += filterDeadzone(Math.round(gp.axes[0] * 100) / 100); // Left JST X
    y1 -= filterDeadzone(Math.round(gp.axes[1] * 100) / 100); // Left JST Y (inverted)
    x2 += filterDeadzone(Math.round(gp.axes[2] * 100) / 100); // Right JST X
    y2 -= filterDeadzone(Math.round(gp.axes[3] * 100) / 100); // Right JST Y (inverted)

    output.innerHTML = `(${x1} \t${y1})\n(${x2} \t${y2}) `;
}

function filterDeadzone(value) {
    const deadzone = 0.05;
    return (Math.abs(value) > deadzone) ? value : 0;
}
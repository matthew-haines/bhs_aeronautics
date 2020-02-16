const WebSocket = require('ws');

var keys = {};
var percentageTexts = new Array();

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function connect(path) {
    const ws = new WebSocket("ws://" + path);
    while (true) {
        await sleep(1000);
        if (ws.readyState === WebSocket.OPEN) {
            console.log("Connected");
            return ws;
        }
    }
}

document.addEventListener("keydown", function onDown(event) {
    keys[event.key.toLowerCase()] = true;
});

document.addEventListener("keyup", function onUp(event) {
    keys[event.key.toLowerCase()] = false;
}); 

function determineCommand(positive, negative) {
    if (positive == negative) return 0;
    else if (positive == undefined) return (negative ? -1 : 0);
    else if (negative == undefined) return (positive ? 1 : 0);
    else if (positive) return 1;
    return -1;
}

function dataSender(client) {
    var message = {
        "time": Math.round((new Date()).getTime()), // in milliseconds since epoch
        "pitch": determineCommand(keys["w"], keys["s"]),
        "yaw": determineCommand(keys['q'], keys['e']),
        "roll": determineCommand(keys['a'], keys['d']),
        "throttle": determineCommand(keys[' '], keys['shift']) // spacebar and shift
    };
    client.send(JSON.stringify(message));
    console.log("Sent");
}

function percentageUpdate(actualValues) {
    for (i = 0; i < 4; i += 1) {
        percentageTexts[i].innerHTML = actualValues[i].toString() + "%";
        console.log(actualValues);
        progressBars[i].setAttribute("style", "width: "+(actualValues[i].toString() + "%;"))
    }
}

function responseHandler(event) {
    console.log("Recieved");
    var data = JSON.parse(event.data);
    motorSpeeds = new Array();
    data.state.motors.forEach(function (item, index) {
        motorSpeeds[index] = item;
    });
    percentageUpdate(motorSpeeds);
}

async function loop(client) {
    while (true) {
        if (client.readyState != 1) {
            console.log("Connection failure");
            return;
        }
        dataSender(client);
        await sleep(50);
    }
}

async function formHandler(form) {
    var ip = form.ip.value;

    if (ip.length == 0) {
        alert("No IP specified");
    }

    var client = await connect(ip);
    document.getElementById("connection-input").setAttribute("style", "border-color: green;");
    
    console.log("Stating loop");
    client.onmessage = responseHandler;
    loop(client);
}

async function setup() {
    console.log("Initializing");
    progressBars = document.getElementsByClassName("progress-bar-percentage");

    for (let wrapper of progressBars) {
        percentageTexts.push(wrapper.getElementsByTagName("span")[0]);
    }
}

window.onload = function() {
    setup();    
}
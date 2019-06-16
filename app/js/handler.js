const WebSocket = require("ws");

var client;
var tasks = {
    "land": false,
    "autohover": false,
    "shutdown": false
}

var keys = {};

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function connect(path) {
    const ws = new WebSocket("ws://" + path);
    return ws;
}


/*var percentageValue = 0;

var progressBars = document.getElementsByClassName("progress-bar-percentage");

var percentages = new Array();
for (let wrapper of progressBars) {
    percentages.push(wrapper.getElementsByTagName("span")[0])
}

async function test() {

    while (true) {
        for (let percentage of percentages) {
            percentage.innerHTML = (percentageValue % 100).toString() + "%";
        }
        for (let progressBar of progressBars) {
            progressBar.setAttribute("style", "width: "+(percentageValue % 100).toString() + "%;");
        }
        percentageValue++;
        await sleep(50);
    }
}

test();*/

function determineCommand(positive, negative) {
    if (positive && negative) return 0;
    else if (positive) return 1;
    return -1;
}

function formHandler(form) {
    var ip = form.ip.value;

    if (ip.length == 0) {
        alert("No IP specified");
        return false;
    }

    client = connect(ip);
    document.getElementById("connection-input").setAttribute("style", "border-color: green;");
    main();
}

function dataSender(event, tasks, client) {
    var message = {
        "time": Math.round((new Date()).getTime() / 1000),
        "commands": {
            "pitch": 0,
            "yaw": 0,
            "roll": 0,
            "throttle": 0
        },
        "tasks": {
            "land": false,
            "autohover": false,
            "shutdown": false
        }
    };

    switch (event.key) {
        case "w":
            message.commands.pitch = 1;
            break;
        case "s":
            message.commands.pitch = -1;
            break;
        case "a":
            message.commands.roll = 1;
            break;
        case "d":
            message.commands.roll = -1;
            break;
        case "q":
            message.commands.yaw = 1;
            break;
        case "e":
            message.commands.yaw = -1;
            break;
    }

    if (event.shiftKey) {
        message.throttle = 1;
    }
    else if (event.altKey) {
        message.throttle = -1;
    }

    message.tasks = tasks;

    client.on("open", function open() {
        ws.send(message);
    })
}

document.addEventListener("keydown", function onDown(event) {
    keys[event.key.toLowerCase()] = true;
});

document.addEventListener("keyup", function onUp(event) {
    keys[event.key.toLowerCase()] = false;
}); 

setTimeout(async function tempPrint() {
    while (true) {
        for (const [key, value] of Object.entries(keys)) {
            if (value == true && key != "dead") {
                console.log(key);
            }
        }
        await sleep(100);
    }
}, 0);

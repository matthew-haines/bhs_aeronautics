const WebSocket = require('ws');

var client;

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function connect(path) {
    const ws = new WebSocket('ws://' + path);
    return ws;
}


/*var percentageValue = 0;

var progressBars = document.getElementsByClassName('progress-bar-percentage');

var percentages = new Array();
for (let wrapper of progressBars) {
    percentages.push(wrapper.getElementsByTagName('span')[0])
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

function main() {

}

function formHandler(form) {
    var ip = form.ip.value;

    if (ip.length == 0) {
        alert('No IP specified');
        return false;
    }

    client = connect(ip);
    document.getElementById('connection-input').setAttribute("style", "border-color: green;");
    main();
}
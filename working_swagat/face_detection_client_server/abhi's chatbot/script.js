function startProgram() {
    var startButton = document.getElementById("startButton");
    var stopButton = document.getElementById("stopButton");

    // Disable the start button and enable the stop button
    startButton.disabled = true;
    stopButton.disabled = false;

    // Send an AJAX request to start the Python program
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/start-program", true);
    xhr.send();
}

function stopProgram() {
    var startButton = document.getElementById("startButton");
    var stopButton = document.getElementById("stopButton");

    // Disable the stop button and enable the start button
    startButton.disabled = false;
    stopButton.disabled = true;

    // Send an AJAX request to stop the Python program
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/stop-program", true);
    xhr.send();
}

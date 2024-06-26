function sendData() {
    const input = document.getElementById('inputField').value;
    fetch('http://your-flask-api-url/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ data: input })
    })
    .then(response => response.json())
    .then(data => {
        displayResult(data);
    })
    .catch(error => console.error('Error:', error));
}

function displayResult(data) {
    const resultDisplay = document.getElementById('resultDisplay');
    resultDisplay.innerHTML = `Server Response: ${data.result}`;
}

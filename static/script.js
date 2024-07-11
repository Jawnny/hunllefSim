const checkboxes = document.querySelectorAll('.weapon-checkbox');
let selectedCheckboxes = [];

checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', () => {
        if (checkbox.checked) {
            selectedCheckboxes.push(checkbox);
            if (selectedCheckboxes.length > 2) {
                const removedCheckbox = selectedCheckboxes.shift();
                removedCheckbox.checked = false;
            }
        } else {
            selectedCheckboxes = selectedCheckboxes.filter(cb => cb !== checkbox);
        }
    });
});

document.getElementById("simulateButton").addEventListener("click", function(event) {
    event.preventDefault(); // Prevent default button behavior

    // Gather input values from the form
    let playerHP = document.getElementById("hpLevel").value;
    let playerAtk = document.getElementById("attackLevel").value;
    let playerStr = document.getElementById("strengthLevel").value;
    let playerDefense = document.getElementById("defenseLevel").value;
    let playerRange = document.getElementById("rangeLevel").value;
    let playerMage = document.getElementById("mageLevel").value;
    let totalFish = document.getElementById("foodCount").value;
    let armorTier = document.querySelector('input[name="armorChoice"]:checked').value;
    let rangePrayer = document.querySelector('input[name="prayerRChoice"]:checked').value;
    let magePrayer = document.querySelector('input[name="prayerMChoice"]:checked').value;
    let meleePrayer = document.querySelector('input[name="prayerMeChoice"]:checked').value;
    let steelSkin = document.getElementById("steelSkin").checked;
    let halberd = document.getElementById("halberd").checked;
    let bow = document.getElementById("bow").checked;
    let staff = document.getElementById("staff").checked;
    let iterations = 1000; // Default iterations or you can add another input for iterations

    // Create a data object to send
    let data = {
        playerHP: parseInt(playerHP),
        playerStr: parseInt(playerStr),
        playerAtk: parseInt(playerAtk),
        playerDefense: parseInt(playerDefense),
        playerRange: parseFloat(playerRange),
        playerMage: parseFloat(playerMage),
        magePrayer: parseFloat(magePrayer),
        rangePrayer: parseFloat(rangePrayer),
        meleePrayer: parseFloat(meleePrayer),
        steelSkin: steelSkin,
        halberd: halberd,
        bow: bow,
        staff: staff,
        armorTier: parseInt(armorTier),
        totalFish: parseInt(totalFish),
        iterations: parseInt(iterations)
    };

    // Send a POST request to the Flask server
    fetch('/simulate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        // Handle the result here, for example:
        document.getElementById("survivalOddsValue").innerText = `${result.survival_odds}%`;
    })
    .catch(error => {
        console.error('Error:', error);
    });
});

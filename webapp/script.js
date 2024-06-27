document.getElementById("simulateButton").addEventListener("click", function(event) {
    event.preventDefault(); // Prevent default button behavior

    // Gather input values from the form
    let playerHP = document.getElementById("hpLevel").value;
    let playerDefense = document.getElementById("defenseLevel").value;
    let playerRange = document.getElementById("rangeLevel").value;
    let playerMage = document.getElementById("mageLevel").value;
    let totalFish = document.getElementById("foodCount").value;
    let armorTier = document.querySelector('input[name="armorChoice"]:checked').value;
    let rangePrayer = document.querySelector('input[name="prayerRChoice"]:checked').value;
    let magePrayer = document.querySelector('input[name="prayerMChoice"]:checked').value;
    let defensePrayer = document.getElementById("optionalBuff").checked ? document.getElementById("optionalBuff").value : 1.0;
    let iterations = 1000; // Default iterations or you can add another input for iterations

    // Print some variables to the console
    console.log("Player HP Level:", playerHP);
    console.log("Player Defense Level:", playerDefense);
    console.log("Player Range Level:", playerRange);
    console.log("Player Mage Level:", playerMage);
    console.log("Armor Tier:", armorTier);
    console.log("Total Fish:", totalFish);
    console.log("Range Prayer:", rangePrayer);
    console.log("Mage Prayer:", magePrayer);
    console.log("Defense Prayer:", defensePrayer);
    console.log("Iterations:", iterations);

    // Create a data object to send
    let data = {
        playerHP: parseInt(playerHP),
        playerDefense: parseInt(playerDefense),
        playerRange: parseFloat(playerRange),
        playerMage: parseFloat(playerMage),
        magePrayer: parseFloat(magePrayer),
        rangePrayer: parseFloat(rangePrayer),
        defensePrayer: parseFloat(defensePrayer),
        armorTier: parseInt(armorTier),
        totalFish: parseInt(totalFish),
        iterations: parseInt(iterations)
    };

    // Send a POST request to the Flask server
    fetch('http://127.0.0.1:5000/simulate', {
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

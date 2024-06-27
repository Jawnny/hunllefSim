from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import math

app = Flask(__name__)
CORS(app) 

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json

    playerHP = int(data["playerHP"])
    playerDefense = int(data["playerDefense"])
    playerRange = float(data["playerRange"])
    playerMage = float(data["playerMage"])
    magePrayer = float(data["magePrayer"])
    rangePrayer = float(data["rangePrayer"])
    defensePrayer = float(data["defensePrayer"])
    armorTier = int(data["armorTier"])
    totalFish = int(data["totalFish"])
    iterations = int(data["iterations"])

    if armorTier == 1:
        armorTierOff = 16
        armorTierDef = 166
        hunllefMax = 13
    elif armorTier == 2:
        armorTierOff = 28
        armorTierDef = 224
        hunllefMax = 10
    elif armorTier == 3:
        armorTierOff = 40
        armorTierDef = 284
        hunllefMax = 8

    playerHP = playerHP + totalFish * 20

    hunllefMageLvl = int(249)
    hunllefAtkRoll = hunllefMageLvl * (90 + 64)
    hunllef_effDefM = 240 + 9
    hunllef_defRollM = hunllef_effDefM * (20 + 64)
    hunllef_effDefR = 240 + 9
    hunllef_defRollR = hunllef_effDefR * (20 + 64)
    hunllefHP = float(1000)

    eff_DefLvlM = math.floor(playerMage * magePrayer * .7 + playerDefense * defensePrayer * .3 + 8)
    eff_DefLvlR = math.floor(playerDefense * defensePrayer) + 8

    defRollR = eff_DefLvlR * (armorTierDef + 64)
    if hunllefAtkRoll > defRollR:
        hunllefAccR = 1 - (defRollR + 2) / (2 * (hunllefAtkRoll + 1))
    else:
        hunllefAccR = hunllefAtkRoll / (2 * (defRollR + 1))

    defRollM = eff_DefLvlM * (armorTierDef) + 64
    if hunllefAtkRoll > defRollM:
        hunllefAccM = 1 - (defRollM + 2) / (2 * (hunllefAtkRoll + 1))
    else:
        hunllefAccM = hunllefAtkRoll / (2 * (defRollM + 1))

    eff_OffLvlM = math.floor(playerMage * magePrayer + 8)
    atkRollM = eff_OffLvlM * (184 + armorTierOff + 64)

    eff_OffLvlR = math.floor(playerRange * rangePrayer + 8)
    atkRollR = eff_OffLvlR * (172 + armorTierOff + 64)

    if atkRollR > hunllef_defRollR:
        bowAcc = 1 - (hunllef_defRollR + 2) / (2 * (atkRollR + 1))
    else:
        bowAcc = atkRollR / (2 * (hunllef_defRollR + 1))
    bowMax = math.floor(((eff_OffLvlR * (138 + 64)) / 640) + .5)

    if atkRollM > hunllef_defRollM:
        staffAcc = 1 - (hunllef_defRollM + 2) / (2 * (atkRollM + 1))
    else:
        staffAcc = atkRollM / (2 * (hunllef_defRollM + 1))
    if magePrayer == 1.15:
        staffMax = 39
    elif magePrayer == 1.25:
        staffMax = 40

    playerDeaths = 0
    hunllefDeaths = 0
    weaponCounter = 0
    hunllefCounter = totalFish * 4
    currentIteration = 0
    timer = 0
    maxTime = 0
    minTime = 1000

    coinFlip = random.randint(0, 1)
    weapon = "staff" if coinFlip == 0 else "bow"

    while iterations >= currentIteration:
        while hunllefHP > 0 and playerHP > 0:
            while weaponCounter <= 5 and hunllefHP > 0 and playerHP > 0 and weapon == "staff":
                hitChance = random.random()
                tornadoChance = random.randint(0, 10000)
                weaponCounter += 1
                if hitChance < staffAcc:
                    playerAttack = random.randint(1, staffMax)
                    hunllefHP -= playerAttack
                hunllefCounter += 4
                if weaponCounter == 5:
                    weapon = "bow"
                    weaponCounter = 0
                if hunllefCounter >= 5:
                    hunllefCounter -= 5
                    hunllefHitChance = random.random()
                    if tornadoChance > 580:
                        if random.randint(0, 99) <= 52:
                            if hunllefHitChance < hunllefAccR:
                                hunllefAttack = random.randint(0, hunllefMax)
                                playerHP -= hunllefAttack
                        else:
                            if hunllefHitChance < hunllefAccM:
                                hunllefAttack = random.randint(0, hunllefMax)
                                playerHP -= hunllefAttack
                timer += 2.4
            while weaponCounter <= 5 and hunllefHP > 0 and playerHP > 0 and weapon == "bow":
                hitChance = random.random()
                tornadoChance = random.randint(0, 10000)
                weaponCounter += 1
                if hitChance < bowAcc:
                    playerAttack = random.randint(1, 41)
                    hunllefHP -= playerAttack
                hunllefCounter += 4
                if weaponCounter == 5:
                    weapon = "staff"
                    weaponCounter = 0
                if hunllefCounter >= 5:
                    hunllefCounter -= 5
                    hunllefHitChance = random.random()
                    if tornadoChance > 580:
                        if random.randint(0, 99) <= 49:
                            if hunllefHitChance < hunllefAccR:
                                hunllefAttack = random.randint(0, hunllefMax)
                                playerHP -= hunllefAttack
                        else:
                            if hunllefHitChance < hunllefAccM:
                                hunllefAttack = random.randint(0, hunllefMax)
                                playerHP -= hunllefAttack
                timer += 2.4
            if playerHP <= 0:
                playerDeaths += 1
            if hunllefHP <= 0:
                hunllefDeaths += 1
        if hunllefHP <= 0 or playerHP <= 0:
            currentIteration += 1
            playerHP = 99 + totalFish * 20
            hunllefHP = 1000
            if timer < minTime:
                minTime = timer
            if timer > maxTime:
                maxTime = timer
            timer = 0

    survival_odds = 100 if playerDeaths == 0 else hunllefDeaths / (playerDeaths + hunllefDeaths) * 100
    print(iterations)
    result = {
        "survival_odds": f"{survival_odds:.2f}"
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)

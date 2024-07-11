from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import random
import math
import os  # Import the os module

app = Flask(__name__)
CORS(app) 

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    data = request.json
    # variable intake
    playerHP = int(data["playerHP"])
    playerAtk = int(data["playerAtk"])
    playerStr = int(data["playerStr"])
    playerDefense = int(data["playerDefense"])
    playerRange = float(data["playerRange"])
    playerMage = float(data["playerMage"])
    magePrayer = float(data["magePrayer"])
    rangePrayer = float(data["rangePrayer"])
    meleePrayer = float(data["meleePrayer"])
    steelSkin = bool(data["steelSkin"])
    halberd = bool(data["halberd"])
    bow = bool(data["bow"])
    staff = bool(data["staff"])
    armorTier = int(data["armorTier"])
    totalFish = int(data["totalFish"])
    iterations = int(data["iterations"])
    # gets list of active weapons
    wep_dict = {
        'Halberd': halberd,
        'Bow': bow,
        'Staff': staff,
    }
    activeWeps = [wep for wep, wep_value in wep_dict.items() if wep_value]
    print(activeWeps)

    # logic for defensive prayer value based on selected prayers
    # this is unga bunga and probably has a more efficent solve
    if rangePrayer != 1.25 and magePrayer != 1.25:
        if steelSkin == True:
            defensePrayer = 1.15
        else:
            defensePrayer = 1.0
    if (rangePrayer == 1.25 and magePrayer == 1.25) or (rangePrayer == 1.25 and meleePrayer == 1.25) or meleePrayer== 1.25 and magePrayer == 1.25:
        defensePrayer = 1.25
    if (rangePrayer == 1.25 and magePrayer != 1.25 and meleePrayer != 1.25) or (magePrayer == 1.25 and rangePrayer != 1.25 and meleePrayer != 1.25) or (meleePrayer == 1.25 and rangePrayer != 1.25 and magePrayer != 1.25):
        if steelSkin == True:
            defensePrayer = 1.2
        else:
            defensePrayer = 1.125 
    # armor bonuses
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
    # health pool calc
    playerHP = playerHP + totalFish * 20

    # hunllef calcs
    hunllefMageLvl = int(249)
    hunllefAtkRoll = hunllefMageLvl * (90 + 64)
    hunllef_effDefM = 240 + 9
    hunllef_defRollM = hunllef_effDefM * (20 + 64)
    hunllef_effDefR = 240 + 9
    hunllef_defRollR = hunllef_effDefR * (20 + 64)
    hunllefHP = float(1000)

    # extra mage defensive calcs
    eff_DefLvlM = math.floor(playerMage * magePrayer * .7 + playerDefense * defensePrayer * .3 + 8)
    eff_DefLvl = math.floor(playerDefense * defensePrayer) + 8

    # mage offensive calcs
    eff_OffLvlM = math.floor(playerMage * magePrayer + 8)
    atkRollM = eff_OffLvlM * (184 + armorTierOff + 64)
    # range offensive calcs
    eff_OffLvlR = math.floor(playerRange * rangePrayer + 8)
    atkRollR = eff_OffLvlR * (172 + armorTierOff + 64)
    # melee offensive calcs
    eff_OffLvlStr = math.floor(playerStr * meleePrayer + 8 + 3)
    eff_offLvlAtk = math.floor(math.floor((playerAtk)*meleePrayer)+8)
    atkRollMelee = math.floor(eff_offLvlAtk*(166+armorTierOff+64))
    halberdMax = math.floor((eff_OffLvlStr*(138+64)+320)/640)
    # range accuracy
    defRollR = eff_DefLvl * (armorTierDef + 64)
    if hunllefAtkRoll > defRollR:
        hunllefAccR = 1 - (defRollR + 2) / (2 * (hunllefAtkRoll + 1))
    else:
        hunllefAccR = hunllefAtkRoll / (2 * (defRollR + 1))
    defRollM = eff_DefLvlM * (armorTierDef) + 64
    if hunllefAtkRoll > defRollM:
        hunllefAccM = 1 - (defRollM + 2) / (2 * (hunllefAtkRoll + 1))
    else:
        hunllefAccM = hunllefAtkRoll / (2 * (defRollM + 1))
    # melee accuracy
    if atkRollMelee > hunllef_defRollR:
        halberdAcc = 1 - (hunllef_defRollR + 2) / (2 * (atkRollMelee + 1))
    else:
        halberdAcc = atkRollMelee / (2 * (hunllef_defRollR + 1))

    if atkRollR > hunllef_defRollR:
        bowAcc = 1 - (hunllef_defRollR + 2) / (2 * (atkRollR + 1))
    else:
        bowAcc = atkRollR / (2 * (hunllef_defRollR + 1))
    bowMax = math.floor(((eff_OffLvlR * (138 + 64)) / 640) + .5)
    # mage accuracy
    if atkRollM > hunllef_defRollM:
        staffAcc = 1 - (hunllef_defRollM + 2) / (2 * (atkRollM + 1))
    else:
        staffAcc = atkRollM / (2 * (hunllef_defRollM + 1))
    if magePrayer == 1.15:
        staffMax = 39
    elif magePrayer == 1.25:
        staffMax = 40
    #initializations
    playerDeaths = 0
    hunllefDeaths = 0
    weaponCounter = 0
    hunllefCounter = totalFish * 4
    currentIteration = 0
    timer = 0
    maxTime = 0
    minTime = 1000
    currentWeapon = random.choice(activeWeps)
    wepAcc = {
        'Bow': bowAcc,
        'Staff': staffAcc,
        'Halberd': halberdAcc
    }
    wepMax = {
        'Bow': bowMax,
        'Staff': staffMax,
        'Halberd': halberdMax
    }

    while iterations >= currentIteration:
        while hunllefHP > 0 and playerHP > 0:
            while weaponCounter <= 5 and hunllefHP > 0 and playerHP > 0:
                hitChance = random.random()
                tornadoChance = random.randint(0, 10000)
                weaponCounter += 1
                if hitChance < wepAcc[currentWeapon]:
                    playerAttack = random.randint(1, wepMax[currentWeapon])
                    hunllefHP -= playerAttack
                hunllefCounter += 4
                if weaponCounter == 5:
                    currentWeapon = next(wep for wep in activeWeps if wep != currentWeapon)
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
    result = {
        "survival_odds": f"{survival_odds:.2f}"
    }
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
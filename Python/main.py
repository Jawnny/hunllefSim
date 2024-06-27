import random
import math


# Player stats/prayers
playerHP = int(input("Enter HP Level: "))
playerDefense = int(input("Enter Defense Level: "))
playerRange = float(input("Enter Range Level: "))
playerMage = float(input("Enter Mage Level: "))
magePrayer = float(input("Enter Mage Prayer Mod: "))
rangePrayer = float(input("Enter Range Prayer Mod: "))
defensePrayer = float(input("Enter Defense Prayer Mod: "))

# Armor tier and associated offensive bonus
armorTier = int(input("Enter armor Tier(1, 2, or 3): "))
if armorTier == 1:
    armorTierOff = 16
    armorTierDef = 166
    hunllefMax = 13
if armorTier == 2:
    armorTierOff = 28
    armorTierDef = 224
    hunllefMax = 10
if armorTier == 3:
    armorTierOff = 40
    armorTierDef = 284
    hunllefMax = 8
totalFish = int(input("Enter total fish: "))
playerHP = playerHP + totalFish * 20
iterations = int(input("How many iterations? "))

# Hunllef Stats
hunllefMageLvl = int(249)
hunllefAtkRoll = hunllefMageLvl*(90+64)
hunllef_effDefM = 240+9
hunllef_defRollM = hunllef_effDefM*(20+64)
hunllef_effDefR = 240+9
hunllef_defRollR = hunllef_effDefR*(20+64)
hunllefHP = float(1000)

# Player effective mage and range levels
eff_DefLvlM = math.floor(playerMage*magePrayer*.7+playerDefense*defensePrayer*.3+8)
eff_DefLvlR = math.floor(playerDefense*defensePrayer)+8

# Range defense rolls for armor tiers
defRollR = eff_DefLvlR*(armorTierDef+64)
# Hunllef Range Accuracy 
if hunllefAtkRoll > defRollR:
    hunllefAccR = 1-(defRollR+2)/(2*(hunllefAtkRoll+1)) 
else:
    hunllefAccR = hunllefAtkRoll/(2*(defRollR+1))

# Mage defense rolls for armor tiers
defRollM = eff_DefLvlM*(armorTierDef)+64
# Hunllef Mage Accuracy
if hunllefAtkRoll > defRollM:
    hunllefAccM = 1-(defRollM+2)/(2*(hunllefAtkRoll+1)) 
else:
    hunllefAccM = hunllefAtkRoll/(2*(defRollM+1))

# Player Mage offense rolls
eff_OffLvlM = math.floor(playerMage*magePrayer+8)
atkRollM = eff_OffLvlM * (184+armorTierOff+64)
# Player Range offense rolls
eff_OffLvlR = math.floor(playerRange*rangePrayer+8)
atkRollR = eff_OffLvlR * (172+ armorTierOff +64)

# Bow Accuracy and max hit
if atkRollR > hunllef_defRollR:
    bowAcc = 1-(hunllef_defRollR+2)/(2*(atkRollR+1)) 
else:
    bowAcc = atkRollR/(2*(hunllef_defRollR+1))
bowMax = math.floor(((eff_OffLvlR*(138+64))/640)+.5)

# Staff Accuracy and max hit
if atkRollM > hunllef_defRollM:
    staffAcc = 1-(hunllef_defRollM+2)/(2*(atkRollM+1)) 
else:
    staffAcc = atkRollM/(2*(hunllef_defRollM+1))
if magePrayer == 1.15:
    staffMax = 39
if magePrayer == 1.25:
    staffMax = 40
    
# Misc vars
playerDeaths = 0
hunllefDeaths = 0
weaponCounter = 0
hunllefCounter = totalFish * 4 # grants hunllef attacks to account for food delay
currentIteration = 0
timer = 0
maxTime = 0
minTime = 1000


# 50/50 to pick a starting weapon
coinFlip = random.randint(0, 1)
weapon = ""
if coinFlip == 0:
    weapon = "staff"
if coinFlip == 1:
    weapon = "bow"
    
while iterations >= currentIteration:
    while hunllefHP > 0 and playerHP > 0:
        while weaponCounter <= 5 and hunllefHP > 0 and playerHP > 0 and weapon == "staff":  # switch weapons while player and hunllef are alive

            hitChance = random.random()  # player random roll for hitting
            tornadoChance = random.randint(0, 10000)  # random roll for using tornado
            weaponCounter = weaponCounter + 1  # add +1 to the count; switching weapons at 6

            if hitChance < staffAcc:  # player hit chance, 0000 is 00.00% chance for hit
                playerAttack = random.randint(1, staffMax)  # player damage roll
                hunllefHP = hunllefHP - playerAttack  # remove some hp from hunllef

            hunllefCounter = hunllefCounter + 4  # hunllef attack counter(needs 5>=, 5 tick cycle)

            if weaponCounter == 5: # switches weapons after 6 attacks
                weapon = "bow"
                weaponCounter = 0  # reset weaponCounter after 6 attacks

            if hunllefCounter >= 5:  # check if hunllef can attack
                hunllefCounter = hunllefCounter - 5  # leave remainder
                hunllefHitChance = random.random() # hunllef random roll for hitting
                if tornadoChance > 580:  # tornado use chance, 580 is 5.8% chance
                    # pick between range/mage attack. Slightly more range hits than mage hits since hunllef starts on range.
                    if random.randint(0,99) <= 52: 
                        if hunllefHitChance < hunllefAccR:  # hunllef hit chance, 0000 is 00.00% chance for hit
                            hunllefAttack = random.randint(0, hunllefMax)  # hunllef damage roll
                            playerHP = playerHP - hunllefAttack  # remove some player hp
                    else:
                        if hunllefHitChance < hunllefAccM:  # hunllef hit chance, 0000 is 00.00% chance for hit
                            hunllefAttack = random.randint(0, hunllefMax)  # hunllef damage roll
                            playerHP = playerHP - hunllefAttack  # remove some player hp

            timer = timer + 2.4  # track kill time

        while weaponCounter <= 5 and hunllefHP > 0 and playerHP > 0 and weapon == "bow":
            hitChance = random.random()
            tornadoChance = random.randint(0, 10000)
            weaponCounter = weaponCounter + 1
            if hitChance < bowAcc:
                playerAttack = random.randint(1, 41)
                hunllefHP = hunllefHP - playerAttack
            hunllefCounter = hunllefCounter + 4
            if weaponCounter == 5:
                weapon = "staff"
                weaponCounter = 0  # reset weaponCounter after 6 attacks
            if hunllefCounter >= 5:
                hunllefCounter = hunllefCounter - 5
                hunllefHitChance = random.random()
                if tornadoChance > 580:  # tornado use chance, 580 is 5.8% chance
                    # pick between range/mage attack. Slightly more range hits than mage hits since hunllef starts on range.
                    if random.randint(0,99) <= 49: 
                        if hunllefHitChance < hunllefAccR:  # hunllef hit chance, 0000 is 00.00% chance for hit
                            hunllefAttack = random.randint(0, hunllefMax)  # hunllef damage roll
                            playerHP = playerHP - hunllefAttack  # remove some player hp
                    else:
                        if hunllefHitChance < hunllefAccM:  # hunllef hit chance, 0000 is 00.00% chance for hit
                            hunllefAttack = random.randint(0, hunllefMax)  # hunllef damage roll
                            playerHP = playerHP - hunllefAttack  # remove some player hp
            timer = timer + 2.4
        if playerHP <= 0:  # if player dies add player death count
            playerDeaths = playerDeaths + 1
        if hunllefHP <= 0:  # if hunllef dies add hunllef death count
            hunllefDeaths = hunllefDeaths + 1
    if hunllefHP <= 0 or playerHP <= 0:  # +1 to iteration counter when either object reaches zero HP
        currentIteration = currentIteration + 1
        playerHP = playerHP = 99 + totalFish * 20  # reset player hp
        hunllefHP = 1000  # reset hunllef hp
        if timer < minTime:
            minTime = timer
        if timer > maxTime:
            maxTime = timer
        timer = 0  # reset timer

if playerDeaths > 0:
    print("Your odds of surviving are: " + str(hunllefDeaths/(playerDeaths+hunllefDeaths)*100) + "%")
else:
    print("Your odds of surviving are: 100%")
print("Max seconds taken: " + str(maxTime))
print("Min seconds taken: " + str(minTime))
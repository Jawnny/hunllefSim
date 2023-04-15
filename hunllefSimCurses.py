import random
import math

# initialize variables
playerDeaths = 0
hunllefDeaths = 0
weaponCounter = 0
hunllefHP = float(1000)
hunllefCounter = 0
totalFish = int(input("Enter total fish: "))
playerHP = 99 + totalFish * 20
armorTier = int(input("Enter armor Tier(1, 2, or 3): "))
iterations = int(input("How many iterations? "))
gambit = int(input("Are you gambit flicking? (1 for yes, 0 for no): "))
currentIteration = 0
timer = 0
deflectFlip = 0

# 50/50 to pick a starting weapon
coinFlip = random.randint(0, 1)
weapon = ""
if coinFlip == 0:
    weapon = "staff"
if coinFlip == 1:
    weapon = "bow"
# set armor and accuracy values
if armorTier == 1:
    bowAcc = 6706
    staffAcc = 7044
    if gambit == 1:
        bowAcc = 10000-(10000-bowAcc)/1.08
        staffAcc = 10000-(10000-staffAcc)/1.08
    hunllefAcc = 6491
    hunllefMax = 17
if armorTier == 2:
    bowAcc = 6858
    staffAcc = 7172
    if gambit == 1:
        bowAcc = 10000-(10000-bowAcc)/1.08
        staffAcc = 10000-(10000-staffAcc)/1.08
    hunllefAcc = 5605
    hunllefMax = 10
if armorTier == 3:
    bowAcc = 6993
    staffAcc = 7290
    if gambit == 1:
        bowAcc = 10000-(10000-bowAcc)/1.08
        staffAcc = 10000-(10000-staffAcc)/1.08
    hunllefAcc = 4741
    hunllefMax = 8
while iterations + 1 > currentIteration:
    while hunllefHP > 0 and playerHP > 0:
        while weaponCounter <= 5 and hunllefHP > 0 and playerHP > 0 and weapon == "staff":  # switch weapons while player and hunllef are alive
            hitChance = random.randint(0, 10000)  # player random roll for hitting
            tornadoChance = random.randint(0, 10000)  # random roll for using tornado
            weaponCounter = weaponCounter + 1  # add +1 to the count; switching weapons at 6
            if hitChance < staffAcc:  # player hit chance, 0000 is 00.00% chance for hit
                playerAttack = random.randint(0, 40)  # player damage roll
                hunllefHP = hunllefHP - playerAttack  # remove some hp from hunllef
            hunllefCounter = hunllefCounter + 4  # hunllef attack counter(needs 5>=, 5 tick cycle)
            if weaponCounter == 5: # switches weapons after 6 attacks
                weapon = "bow"
                weaponCounter = 0  # reset weaponCounter after 6 attacks

            if hunllefCounter >= 5:  # check if hunllef can attack
                hunllefCounter = hunllefCounter - 5  # leave remainder
                hunllefHitChance = random.randint(0, 10000)  # hunllef random roll for hitting
                if tornadoChance > 58:  # tornado use chance, 58 is 5.8% chance
                    if hunllefHitChance < hunllefAcc:  # hunllef hit chance, 0000 is 00.00% chance for hit
                        hunllefAttack = random.randint(0, hunllefMax)  # hunllef damage roll
                        deflectDMG = math.floor(hunllefAttack/10)
                        deflectFlip = random.randint(0,1)
                        if deflectFlip > 0:
                            hunllefHP = hunllefHP - deflectDMG
                        playerHP = playerHP - hunllefAttack  # remove some player hp

            timer = timer + 2.4  # track kill time

        while weaponCounter <= 5 and hunllefHP > 0 and playerHP > 0 and weapon == "bow":
            hitChance = random.randint(0, 10000)
            tornadoChance = random.randint(0, 10000)
            weaponCounter = weaponCounter + 1
            if hitChance < bowAcc:
                playerAttack = random.randint(0, 42)
                hunllefHP = hunllefHP - playerAttack
            hunllefCounter = hunllefCounter + 4
            if weaponCounter == 5:
                weapon = "staff"
                weaponCounter = 0  # reset weaponCounter after 6 attacks

            if hunllefCounter >= 5:
                hunllefCounter = hunllefCounter - 5
                hunllefHitChance = random.randint(0, 10000)
                if tornadoChance > 580:  # tornado use chance, 58 is 5.8% chance
                    if hunllefHitChance < hunllefAcc:  # hunllef hit chance, 6363 is 63.63% chance for hit
                        hunllefAttack = random.randint(0, hunllefMax)
                        deflectDMG = math.floor(hunllefAttack/10)
                        deflectFlip = random.randint(0,1)
                        if deflectFlip > 0:
                            hunllefHP = hunllefHP - deflectDMG
                        playerHP = playerHP - hunllefAttack
            timer = timer + 2.4
        if playerHP <= 0:  # if player dies add player death count
            playerDeaths = playerDeaths + 1
            print("Player died")
        if hunllefHP <= 0:  # if hunllef dies add hunllef death count
            hunllefDeaths = hunllefDeaths + 1
            print("Hunllef died")

    if hunllefHP <= 0 or playerHP <= 0:  # +1 to iteration counter when either object reaches zero HP
        currentIteration = currentIteration + 1
        print(currentIteration)  # debug stuff
        playerHP = playerHP = 99 + totalFish * 20  # reset player hp
        hunllefHP = 1000  # reset hunllef hp
        print("Timer: " + str(int(timer)))  # kill time
        timer = 0  # reset timer

print()
print("Armor level: " + str(armorTier))
print("Fish collected: " + str(totalFish))
print("Player deaths: " + str(playerDeaths))
print("Sucessful kills: " + str(hunllefDeaths))

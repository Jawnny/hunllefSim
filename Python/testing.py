import  math
import random

# Player stats/prayers
playerHP = int(input("Enter HP Level: "))
playerDefense = int(input("Enter Defense Level: "))
playerRange = float(input("Enter Range Level: "))
playerMage = float(input("Enter Mage Level: "))
magePrayer = float(input("Enter Mage Prayer: "))
rangePrayer = float(input("Enter Range Prayer: "))
defensePrayer = float(input("Enter Defense Prayer: "))
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

# Bow Accuracy
if atkRollR > hunllef_defRollR:
    bowAcc = 1-(hunllef_defRollR+2)/(2*(atkRollR+1)) 
else:
    bowAcc = atkRollR/(2*(hunllef_defRollR+1))
bowMax = 41
# Staff Accuracy
if atkRollM > hunllef_defRollM:
    staffAcc = 1-(hunllef_defRollM+2)/(2*(atkRollM+1)) 
else:
    staffAcc = atkRollM/(2*(hunllef_defRollM+1))
staffMax = 40
# Misc vars
playerDeaths = 0
hunllefDeaths = 0
weaponCounter = 0
hunllefCounter = 0
currentIteration = 0
timer = 0


print(staffAcc)
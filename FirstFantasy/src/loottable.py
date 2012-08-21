'''
Last changed by: Dale Everett
'''
import items
import random
from weightedchoice import weighted_choice_sub
            

def createUnique(quality):
    """Chooses an unique item"""
    unique_list = (items.Sword("Sword of a Thousand Truths",[2,2,2,2]),items.Armor("Judgement Chestguard","Chest",[3,1,3,1]))
    return random.choice(unique_list)

def Loot(level):
    """Decides loot given for the kill"""
    gold = random.randint(0,10) * level + 10
    
    quality = level // 4
    
    item_type_list = ("None",2), ("Armor",10), ("Weapon",7), ("Consumable",7), ("Rare",100) #100 Rare weight is for testing
    item_type = item_type_list[weighted_choice_sub([x[1] for x in item_type_list])][0]
    
    if item_type == "Consumable":
        item = createConsumable(quality)
    elif item_type == "Armor":
        item = createArmor(quality)
    elif item_type == "Weapon":
        item = createWeapon(quality)
    elif item_type == "Rare":
        item = createUnique(quality)
    else:
        item = None
    
    return (gold, item)

armor_slots = ("Helm","Coat","Gloves","Leggings","Boots")
weapon_types = ("Sword","Right Hand",[1,0,0,0]), ("Mace","Right Hand",[0,0,1,0]), ("Dagger","Right Hand",[0,1,0,0]) 
weapon_prefixes = ("",10,[0,0,0,0]), ("Sharp ",1,[1,1,0,0]), ("Precise ",1,[0,1,1,0]), ("Stalwart ",1,[0,0,1,1]), ("Unyielding ",1,[1,0,0,1])
armor_prefixes = ("Crude ",[0,0,1,0]), ("Basic ",[0,0,2,0]), ("Sturdy ",[0,0,2,1])
suffixes = (("",(10,[0,0,0,0])), (" of Brutality",(1,[1,1,0,0])), (" of Survival",(1,[0,0,1,1])), (" of Finesse",(1,[0,1,1,0])), (" of Dueling",(1,[1,0,0,1])))

def createArmor(quality,armor_slot = ""):
    """Creates a piece of armor"""
    stats = []
    
    if armor_slot == "":
        slot = random.choice(armor_slots)
    else:
        slot = armor_slot
    prefix = armor_prefixes[quality]
    suffix = suffixes[weighted_choice_sub([x[1][0] for x in suffixes])]
    name = prefix[0] + slot + suffix[0]
    for i in range(4):
        stats.append(prefix[1][i] + suffix[1][1][i])
        
    return items.Armor(name,slot,stats)

def createWeapon(quality,weapon_type = ""):
    """Creates a weapon"""
    stats = []
    
    if weapon_type == "":
        w_type = random.choice(weapon_types)
    else:
        w_type = weapon_type
    
    prefix = weapon_prefixes[weighted_choice_sub([x[1] for x in weapon_prefixes])]
    name = prefix[0] + w_type[0]
    for i in range(4):
        stats.append((prefix[2][i] + w_type[2][i]) * (1 + quality))
        
    if w_type[0] == "Sword":
        return items.Sword(name,stats)
    if w_type[0] == "Mace":
        return items.Mace(name,stats)
    if w_type[0] == "Dagger":
        return items.Dagger(name,stats)
    
def createConsumable(quality):
    """Chooses a consumable"""
    consumable_weights = (10,2)
    choice = weighted_choice_sub(consumable_weights)
    if choice == 0:
        return items.SmallHealthPotion()
    elif choice == 1:
        return items.SmallExperienceBoost()    
from weightedchoice import weighted_choice_sub
import random
import math
import items
import loottable
import inventory
import os


class Character:
    # Defines an interactive character within the game
    def __init__(self, name, base_attributes, level = 0, ):
        self.status = ["normal"]
        self.name = name
        self.equipped_gear = inventory.Equipment(self)
        self.character_attributes = base_attributes
        self.total_attributes = {}
        self.attribute_bonuses = {"Base Damage" : ["Strength", 1/5, 0],
                                    "HP" : ["Strength", 3, 0],
                                    "Physical Resist": ["Strength", 1/1000, 0],
                                    "Random Damage" : ["Dexterity", 1/5, 0],
                                    "Crit Rate" : ["Dexterity", 1/1000, 0],
                                    "Evasion" : ["Dexterity", 1/1000, 0],
                                    "Magic Damage" : ["Intelligence", 1/5, 0],
                                    "Mana Regen" : ["Intelligence", 1/3, 0],
                                    "Magical Resist" : ["Intelligence", 1/1000, 0]
                                    }
        self.total_modifiers = {}
        self.health = 0
        self.level = level

    def update(self):
        self.updateTotalAttributes()
        self.updateBonuses()
        self.updateTotalModifiers()

    def updateTotalModifiers(self):
        new_total_modifiers = {}
        new_total_modifiers.update(self.equipped_gear.getModifiers())

        for modifier in self.attribute_bonuses:
            if modifier in new_total_modifiers:
                new_total_modifiers[modifier] += self.attribute_bonuses[modifier][2]
            else:
                new_total_modifiers.update({modifier:self.attribute_bonuses[modifier][2]})
        self.total_modifiers = new_total_modifiers

    def updateBonuses(self):
        for bonus in self.attribute_bonuses.values():
            bonus[2] = self.total_attributes[bonus[0]] * bonus[1]
        

    def updateTotalAttributes(self):
        new_total_attributes = {}
        new_total_attributes.update(self.character_attributes)
        gear_attributes = self.equipped_gear.getAttributes()
        
        new_total_attributes["Strength"] += gear_attributes["Strength"]
        new_total_attributes["Dexterity"] += gear_attributes["Dexterity"]
        new_total_attributes["Intelligence"] += gear_attributes["Intelligence"]

        self.total_attributes = new_total_attributes

    def getMaxHealth(self):
        return self.total_modifiers["HP"]

    def getPhysResist(self):
        return self.total_modifiers["Physical Resist"]
    
    def getMagResist(self):
        return self.total_modifiers["Magical Resist"]
    
    def getEvasionRate(self):
        return self.total_modifiers["Evasion"]

    def showStringWeaponDamage(self):
        base_dmg = self.total_modifiers["Base Damage"]
        random_dmg = self.total_modifiers["Random Damage"]
        random_mult = self.total_modifiers["Random Multiplier"]
        return "{} + ({} to {})".format(base_dmg, random_mult, random_dmg * random_mult)
    
    def getCritRate(self):
        return self.total_modifiers["Crit Rate"]

    def getCritMult(self):
        return self.total_modifiers["Crit Multiplier"]
    
    def getCharacterSheet(self):
        print("[---Character Sheet---]")
        print("Name: %s (Level: %d)" % (self.name, self.level))
        print("Health: %d/%d" % (self.health, self.getMaxHealth()))
        print("\nStrength: {}".format(self.character_attributes["Strength"]))
        print("Dexterity: {}".format(self.character_attributes["Dexterity"]))
        print("Intelligence: {}".format(self.character_attributes["Intelligence"]))
        print("\nAttack: {}".format(self.showStringWeaponDamage()))
        print("Crit Chance: {:.2%}".format(self.getCritRate()))

        print("\nPhysical Resist: {:.2%}".format(self.getPhysResist()))
        print("Magical Resist: {:.2%}".format(self.getMagResist()))
        print("Evasion Chance: {:.2%}".format(self.getEvasionRate()))

    def takeDamage(self, damage):
        damage -= round(damage * self.getPhysResist())
        self.health -= round(damage)
        if self.health <= 0:
            self.status.append("dead")
            self.health = 0

class Enemy(Character):
    # Enemy object
    def __init__(self, 
                 name, 
                 level, 
                 attribute_weights,
                 weapon_modifiers,
                 attributes = None):
        if attributes == None:
            attributes = {"Strength" : attribute_weights[0],
                          "Dexterity" : attribute_weights[1],
                          "Intelligence" : attribute_weights[2]}
        super().__init__(name, attributes, level)
        self.att_weights = attribute_weights
        self.initLevel(self.level * 8)
        self.update()
        self.health = self.getMaxHealth()
        self.loot_table = loottable.LootGenerator(level, self)
        self.weapon = items.Weapon("", weapon_modifiers)
    
    def initLevel(self, amount):
        key_list = random.choices(list(self.character_attributes.keys()), self.att_weights, k=amount)
        for att in key_list:
            self.character_attributes[att] += 1

    def attack(self, receiver):
        if random.random() <= receiver.getEvasionRate():
            print("{} missed their attack!")
        else:
            weapon_damage = self.weapon.getCalculatedDamage(self)
            if random.random() <= self.getCritRate():
                print("CRITICAL STRIKE!!!")
                weapon_damage *= self.getCritMult()
            round(weapon_damage)

            print(self.name + " attacked for " + repr(weapon_damage) +
                " (-{})".format(round(weapon_damage * receiver.getPhysResist())))
            receiver.takeDamage(weapon_damage)


class Player(Character):
    # Player object
    def __init__(self, name, 
                 level = 1,
                 attributes = {"Strength" : 10,
                               "Dexterity" : 10, 
                               "Intelligence" : 10}):
        super().__init__(name, attributes, level)
        self.gold = 0
        self.exp = 0
        self.exp_needed = 1000
        self.inventory = inventory.Storage(10, self)
        self.update()
        self.health = self.getMaxHealth()

    def giveExp(self, exp_earned):
        # Gives the player exp_earned experience and checks for level up
        print(self.name + " gained " + repr(exp_earned) + " experience!")
        self.exp += exp_earned
        self.checkLevelUp()

    def giveHealth(self, given_health):
        self.health += given_health
        if self.health > self.getMaxHealth():
            self.health = self.getMaxHealth()
        if "dead" in self.status:
            self.status.remove("dead")

    def giveGold(self, gold_earned):
        print(self.name + " gained " + repr(gold_earned) + " gold!")
        self.gold += gold_earned

    def takeGold(self, gold_taken=0):
        if self.gold < gold_taken:
            if "dead" in self.status:
                self.gold = 0
                print("You've lost all your gold!")
                return False
            else:
                print("You do not have enough gold!")
                return False
        else:
            self.gold -= gold_taken
            print(self.name + " lost " + repr(gold_taken) + " gold!")
            return True

    def giveItem(self, item):
        # Checks to see if inventory has space and gives item to player
        print(self.name + " received a " + item.name + "!")
        self.inventory.add(item)

    def getInventory(self, from_where="zone"):
        # Displays inventory and options
        if self.inventory.isEmpty():
            input("Your inventory is empty.\n" +
                      "Press enter to continue...")
            return

        while True:
            accessed_item = self.inventory.access(from_where)
            if accessed_item is False:
                break
            os.system("cls" if os.name == "nt" else "clear")

            item_choice = accessed_item.getOptions(from_where)

            if item_choice == "equip":
                unequipped_item = self.equipped_gear.equip(accessed_item,
                                                    self.inventory,
                                                    from_where)
                if unequipped_item is not False:
                    self.inventory.remove(accessed_item)
                    self.update()
                break
            elif item_choice == "consume":
                self.inventory.use(accessed_item, self)             
                input("Press \"Enter\" to continue...")
                break
            elif item_choice == "destroy":
                self.inventory.remove(accessed_item)

    def attack(self, receiver):
        if random.random() <= receiver.getEvasionRate():
            print("{} missed their attack!".format(self.name))
        else:
            weapon_damage = self.equipped_gear.get("Main Hand").getCalculatedDamage(self)

            if random.random() <= self.getCritRate():
                print("CRITICAL STRIKE!!!")
                weapon_damage *= self.getCritMult()
            round(weapon_damage)
            
            print(self.name + " attacked for " + repr(weapon_damage) +
                " (-{})".format(round(weapon_damage * receiver.getPhysResist())))
            receiver.takeDamage(weapon_damage)

    def checkLevelUp(self):
        # Checks to see if enough experience has been gained to level up
        level_gain = 0
        while self.exp >= self.exp_needed:
            print("\nLevel up!!!")
            self.level += 1
            self.exp -= self.exp_needed
            self.exp_needed += self.level * 100
            level_gain += 1
        if level_gain > 0:
            input("Press \"Enter\" to continue...")
            os.system("cls" if os.name == "nt" else "clear")
            self.levelUp(level_gain)

    def levelUp(self, level_gain):
        # Allocate points to attributes
        points_gain = level_gain * 5
        while points_gain != 0:

            print("Points available: ", points_gain)
            print("[------------------]")
            print("(1) Strength: ", self.character_attributes["Strength"])
            print("(2) Dexterity: ", self.character_attributes["Dexterity"])
            print("(3) Intelligence: ", self.character_attributes["Intelligence"])
            choice = input("Place point into: ")
            if choice == '1':
                self.character_attributes["Strength"] += 1
            elif choice == '2':
                self.character_attributes["Dexterity"] += 1
            elif choice == '3':
                self.character_attributes["Intelligence"] += 1
            else:
                continue
            points_gain -= 1
            self.health = self.getMaxHealth()
            self.update()
            os.system("cls" if os.name == "nt" else "clear")

    def getCharacterSheet(self):
        # Print Character stats and equipped gear
        print("[---Character Sheet---]")
        print("Name: %s (Level: %d)" % (self.name, self.level))
        print("Health: %d/%d" % (self.health, self.getMaxHealth()))
        print("Gold: %d" % (self.gold))
        print("Exp: %d/%d" % (self.exp, self.exp_needed))
        print("\nStrength: {}".format(self.total_attributes["Strength"]))
        print("Dexterity: {}".format(self.total_attributes["Dexterity"]))
        print("Intelligence: {}".format(self.total_attributes["Intelligence"]))
        print("\nAttack: {}".format(self.showStringWeaponDamage()))
        print("Crit Chance: {:.2%}".format(self.getCritRate()))
        print("\nPhysical Resist: {:.2%}".format(self.getPhysResist()))
        print("Magical Resist: {:.2%}".format(self.getMagResist()))
        print("Evasion Chance: {:.2%}".format(self.getEvasionRate()))

        print("\n[------Equipment-----]")
        for x in self.equipped_gear.slots_dict:
            if self.equipped_gear.slots_dict.get(x) is not None:
                name = self.equipped_gear.slots_dict.get(x).name
            else:
                name = "None"
            print("{}: {}".format(x, name))

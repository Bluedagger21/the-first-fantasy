from weightedchoice import weighted_choice_sub
import random
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
        self.attributes = base_attributes
        self.total_attributes = None
        self.attribute_bonuses = {"str_base_dmg" : ["Strength", 1/5, 0],
                                    "str_hp" : ["Strength", 3, 0],
                                    "str_phy_resist": ["Strength", 1/10, 0],
                                    "dex_rnd_dmg" : ["Dexterity", 1/5, 0],
                                    "dex_crit_rate" : ["Dexterity", 1/10, 0],
                                    "dex_eva" : ["Dexterity", 1/10, 0],
                                    "int_mag_dmg" : ["Intelligence", 1/5, 0],
                                    "int_mana_regen" : ["Intelligence", 1/3, 0],
                                    "int_mag_resist" : ["Intelligence", 1/10, 0]
                                    }
        self.health = 0
        self.level = level

    def update(self):
        self.updateTotalAttributes()
        self.updateBonuses()

    def updateBonuses(self):
        for bonus in self.attribute_bonuses.values():
            bonus[2] = self.total_attributes[bonus[0]] * bonus[1]

    def updateTotalAttributes(self):
        self.total_attributes = self.attributes
        gear_attributes = self.equipped_gear.getAttributes()
        
        self.total_attributes["Strength"] += gear_attributes["Strength"]
        self.total_attributes["Dexterity"] += gear_attributes["Dexterity"]
        self.total_attributes["Intelligence"] += gear_attributes["Intelligence"]


    def getMaxHealth(self):
        return self.attribute_bonuses["str_hp"][2]

    def getPhysResist(self):
        return (self.attribute_bonuses["str_phy_resist"][2] / 100)

    def showStringWeaponDamage(self):
        base_dmg = self.equipped_gear.slots_dict["Main Hand"].base_damage
        random_dmg = self.equipped_gear.slots_dict["Main Hand"].random_damage
        random_mult = self.equipped_gear.slots_dict["Main Hand"].random_mult
        return "{} + ({} to {})".format(base_dmg, random_mult, random_dmg)
    
    def getCritRate(self):
        return self.equipped_gear.slots_dict["Main Hand"].base_crit_rate + \
            (self.attribute_bonuses["dex_crit_rate"][2] / 100)

    def getCritMult(self):
        return self.equipped_gear.slots_dict["Main Hand"].crit_mult
    
    def getCharacterSheet(self):
        print("[---Character Sheet---]")
        print("Name: %s (Level: %d)" % (self.name, self.level))
        print("Health: %d/%d" % (self.health, self.getMaxHealth()))
        print("\nStrength: {}".format(self.attributes["Strength"]))
        print("Dexterity: {}".format(self.attributes["Dexterity"]))
        print("Intelligence: {}".format(self.attributes["Intelligence"]))
        print("\nAttack: {}".format(self.showStringWeaponDamage()))
        print("Crit Chance: {:.2%}".format(self.getCritRate()))
        print("Physical Resist: {:.2%}".format(self.getPhysResist()))

    def attack(self, receiver):
        damage = self.getDamage()
        receiver.takeDamage(damage)
        print(self.name + " attacked for " + repr(damage) +
              " (-{})".format(round(damage * receiver.getArmorReduce())))

    def takeDamage(self, damage):
        damage -= round(damage * self.getPhysResist())
        self.health -= round(damage)
        if self.health <= 0:
            self.status.append("dead")
            self.health = 0

    def getDamage(self):
        damage = self.getAttackDamage()
        if random() <= self.getCritRate():
            print("CRITICAL STRIKE!!!")
            damage *= 2
        return round(damage)


class Enemy(Character):
    # Enemy object
    def __init__(self, name, level, attribute_weights, attributes = {"Strength" : 0,
                                                                     "Dexterity" : 0,
                                                                     "Intelligence" : 0}):
        super().__init__(name, attributes, level)
        self.att_weights = attribute_weights
        self.initLevel(self.level * 10)
        self.update()
        self.health = self.getMaxHealth()
        self.loot_table = loottable.LootGenerator(level, self)

    def initLevel(self, amount):
        key_list = random.choices(list(self.attributes.keys()), self.att_weights, k=amount)
        for att in key_list:
            self.attributes[att] += 1

class Player(Character):
    # Player object
    def __init__(self, name, 
                 level = 0,
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
                    self.updateEquipmentStats()
                break
            elif item_choice == "consume":
                self.inventory.use(accessed_item, self)             
                input("Press \"Enter\" to continue...")
                break
            elif item_choice == "destroy":
                self.inventory.remove(accessed_item)

    def attack(self, receiver):
        weapon_damage = self.equipped_gear.get("Main Hand").getCalculatedDamage(self)
        if random.random() <= self.getCritRate():
            print("CRITICAL STRIKE!!!")
            weapon_damage *= self.getCritMult()
        round(weapon_damage)

        print(self.name + " attacked for " + repr(weapon_damage) +
              " (-{})".format(round(weapon_damage * ((1 + receiver.getPhysResist())/100))))
        receiver.takeDamage(weapon_damage)

    def updateEquipmentStats(self):
        # Updates equipment stats after changing equipment
        for i in range(len(self.equipment_stat_list)):
            tmp_amount = 0
            for x in self.equipped_gear.slots_dict.values():
                if x is not None:
                    tmp_amount += x.stats[i]
                else:
                    tmp_amount += 0
            for x in self.equipped_gear.slots_dict.values():
                if x is not None:
                    tmp_amount += x.stats[i]
                else:
                    tmp_amount += 0
            self.equipment_stat_list[i] = tmp_amount

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
            print("(1) Power: ", self.stat_list[0])
            print("(2) Precision: ", self.stat_list[1])
            print("(3) Toughness: ", self.stat_list[2])
            print("(4) Vitality: ", self.stat_list[3])
            choice = input("Place point into: ")
            if choice == '1':
                self.stat_list[0] += 1
            elif choice == '2':
                self.stat_list[1] += 1
            elif choice == '3':
                self.stat_list[2] += 1
            elif choice == '4':
                self.stat_list[3] += 1
            else:
                continue
                os.system("cls" if os.name == "nt" else "clear")
            points_gain -= 1
            self.health = self.getMaxHealth()
            os.system("cls" if os.name == "nt" else "clear")

    def getCharacterSheet(self):
        # Print Character stats and equipped gear
        print("[---Character Sheet---]")
        print("Name: %s (Level: %d)" % (self.name, self.level))
        print("Health: %d/%d" % (self.health, self.getMaxHealth()))
        print("Gold: %d" % (self.gold))
        print("Exp: %d/%d" % (self.exp, self.exp_needed))
        print("\nStrength: {}".format(self.attributes["Strength"]))
        print("Dexterity: {}".format(self.attributes["Dexterity"]))
        print("Intelligence: {}".format(self.attributes["Intelligence"]))
        print("\nAttack: {}".format(self.showStringWeaponDamage()))
        print("Crit Chance: {:.2%}".format(self.getCritRate()))
        print("Physical Resist: {:.2%}".format(self.getPhysResist()))

        print("\n[------Equipment-----]")
        for x in self.equipped_gear.slots_dict:
            if self.equipped_gear.slots_dict.get(x) is not None:
                name = self.equipped_gear.slots_dict.get(x).name
            else:
                name = "None"
            print("{}: {}".format(x, name))

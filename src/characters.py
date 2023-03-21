from weightedchoice import weighted_choice_sub
import random
import math
import mastery
import items
import loottable
import inventory
import os


class Character:
    # Defines an interactive character within the game
    def __init__(self, name, stats, level = 0, ):
        self.status = ["normal"]
        self.name = name
        self.equipped_gear = inventory.Equipment(self)
        self.base_stats = stats
        self.stats = self.base_stats
        self.level = level
        self.health = self.stats["Vitality"] * 2

    def getMaxHealth(self):
        return (self.stats["Vitality"] * 2) + (10 * self.level)
    
    def getCharacterSheet(self):
        print("[---Character Sheet---]")
        print("Name: %s (Level: %d)" % (self.name, self.level))
        print("Health: %d/%d" % (self.health, self.getMaxHealth()))
        print("\nVitality: {}".format(self.stats["Vitality"]))
        print("Physical Resist: {:.2%}".format(self.stats["Physical Resist"]))
        print("Magical Resist: {:.2%}".format(self.stats["Magical Resist"]))
        print("\nBase Weapon Damage: {}".format(self.stats["Base Weapon Damage"]))
        print("Power: {}".format(self.stats["Power"]))

    def takeDamage(self, damage, dealer):
        if "parry" in self.status:
            self.equipped_gear["Main Hand"].triggerParry(self, dealer, damage)
        else:
            print("{} takes {} damage.".format(self.name, damage))
            self.health -= damage
            if self.health <= 0:
                self.status.append("dead")
                self.health = 0

class Player(Character):
    # Player object
    def __init__(self, name, 
                 level=1,
                 stats={"Vitality": 10,
                        "Physical Resist": 0,
                        "Magical Resist": 0,
                        "Power": 0}):
        super().__init__(name, stats, level)
        self.gold = 0
        self.exp = 0
        self.exp_needed = 1000
        self.inventory = inventory.Storage(10, self)
        self.updateStats()
        self.health = self.getMaxHealth()
        self.sword_mastery = mastery.Mastery(items.Sword)

    def updateStats(self):
        gear_stats = self.equipped_gear.getStats()
        new_stats = self.base_stats

        for stat in gear_stats:
            if stat not in new_stats:
                new_stats.update({stat: gear_stats[stat]})
            else:
                new_stats[stat] += gear_stats[stat]

        return new_stats

    def giveXP(self, exp_earned):
        # Gives the player exp_earned experience and checks for level up
        print(self.name + " gained " + repr(exp_earned) + " experience!")
        self.exp += exp_earned

        if isinstance(items.Sword, self.equipped_gear.get("Main Hand")):
            self.sword_mastery.giveXP(exp_earned)

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
        self.equipped_gear["Main Hand"].use(self, receiver)

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
        print("\nVitality: {}".format(self.stats["Vitality"]))
        print("Physical Resist: {:.2%}".format(self.stats["Physical Resist"]))
        print("Magical Resist: {:.2%}".format(self.stats["Magical Resist"]))
        print("\nBase Weapon Damage: {}".format(self.stats["Base Damage"]))
        print("Power: {}".format(self.stats["Power"]))

        print("\n[------Equipment-----]")
        for x in self.equipped_gear.slots_dict:
            if self.equipped_gear.slots_dict.get(x) is not None:
                name = self.equipped_gear.slots_dict.get(x).name
            else:
                name = "None"
            print("{}: {}".format(x, name))

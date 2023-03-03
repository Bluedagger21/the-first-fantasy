from weightedchoice import weighted_choice_sub
from random import random
import items
import inventory
import os


class Character:
    # Defines an interactive character within the game
    def __init__(self):
        self.status = ["normal"]
        self.VITALITY_RATIO = 5
        self.POWER_RATIO = 1.5
        self.name = ""
        self.health = 5
        self.stat_list = [5, 7, 7, 5]
        self.equipment_stat_list = [0, 0, 0, 0]
        self.level = 1

    def getMaxHealth(self):
        return ((self.stat_list[3] + self.equipment_stat_list[3]) *
                 self.VITALITY_RATIO)

    def getCritChance(self):
        return (0.1 * ((self.stat_list[1] + self.equipment_stat_list[1]) /
                      ((self.level * 2.0) + 8.0)))

    def getArmorReduce(self):
        return (0.1 * ((self.stat_list[2] + self.equipment_stat_list[2]) /
                      ((self.level * 3.0) + 7.0)))

    def getAttackDamage(self):
        return ((self.stat_list[0] + self.equipment_stat_list[0]) *
                 self.POWER_RATIO)

    def getCharacterSheet(self):
        print("[---Character Sheet---]")
        print("Name: %s (Level: %d)" % (self.name, self.level))
        print("Health: %d/%d" % (self.health, self.getMaxHealth()))
        print("\nPower: %d" % (self.stat_list[0]))
        print("Precision: %d" % (self.stat_list[1]))
        print("Toughness: %d" % (self.stat_list[2]))
        print("Vitality: %d" % (self.stat_list[3]))
        print("\nAttack: %d" % (self.getAttackDamage()))
        print("Crit Chance: {:.2%}".format(self.getCritChance()))
        print("Armor: {:.2%}".format(self.getArmorReduce()))

    def attack(self, receiver):
        damage = self.getDamage()
        receiver.takeDamage(damage)
        print(self.name + " attacked for " + repr(damage) +
              " (-{})".format(round(damage * receiver.getArmorReduce())))

    def takeDamage(self, damage):
        damage -= round(damage * self.getArmorReduce())
        self.health -= round(damage)
        if self.health <= 0:
            self.status.append("dead")
            self.health = 0

    def getDamage(self):
        damage = self.getAttackDamage()
        if random() <= self.getCritChance():
            print("CRITICAL STRIKE!!!")
            damage *= 2
        return round(damage)


class Enemy(Character):
    # Enemy object
    def __init__(self, name, stats, level):
        Character.__init__(self)
        self.name = name
        self.level = level
        self.stat_weights = stats
        self.initLevel(level * 5)
        self.health = self.getMaxHealth()

    def initLevel(self, level):
        for _ in range(level - 1):
            tmp_index = weighted_choice_sub(self.stat_weights)
            self.stat_list[tmp_index] += 1


class Player(Character):
    # Player object
    def __init__(self, playername):
        Character.__init__(self)
        self.name = playername
        self.level = 1
        self.gold = 0
        self.exp = 0
        self.exp_needed = 1000
        self.stat_list = [10, 10, 10, 10]
        self.equipment_stat_list = [0, 0, 0, 0]
        self.inventory = inventory.Storage(10, self)
        self.equipped_gear = inventory.Equipment(self)
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
        self.equipped_gear.get("Right Hand").attack(self, receiver)

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
        print("\nPower: {} (+{})".format(self.stat_list[0] +
                                         self.equipment_stat_list[0],
                                         self.equipment_stat_list[0]))
        print("Precision: {} (+{})".format(self.stat_list[1] +
                                           self.equipment_stat_list[1],
                                           self.equipment_stat_list[1]))
        print("Toughness: {} (+{})".format(self.stat_list[2] +
                                           self.equipment_stat_list[2],
                                           self.equipment_stat_list[2]))
        print("Vitality: {} (+{})".format(self.stat_list[3] +
                                          self.equipment_stat_list[3],
                                          self.equipment_stat_list[3]))
        print("\nAttack: %d" % (self.getAttackDamage()))
        print("Crit Chance: {:.2%}".format(self.getCritChance()))
        print("Armor: {:.2%}".format(self.getArmorReduce()))

        print("\n[------Equipment-----]")
        for x in self.equipped_gear.slots_dict:
            if self.equipped_gear.slots_dict.get(x) is not None:
                name = self.equipped_gear.slots_dict.get(x).name
            else:
                name = "None"
            print("{}: {}".format(x, name))

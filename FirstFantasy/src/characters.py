'''
Last changed by: Ryan Breaker
'''
from weightedchoice import weighted_choice_sub
from random import random
import items
import os


class Character:
    """Defines an interactive character within the game"""
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
        print ("[---Character Sheet---]")
        print ("Name: %s (Level: %d)" % (self.name, self.level))
        print ("Health: %d/%d" % (self.health, self.getMaxHealth()))
        print ("\nPower: %d" % (self.stat_list[0]))
        print ("Precision: %d" % (self.stat_list[1]))
        print ("Toughness: %d" % (self.stat_list[2]))
        print ("Vitality: %d" % (self.stat_list[3]))
        print ("\nAttack: %d" % (self.getAttackDamage()))
        print ("Crit Chance: {:.2}%".format(self.getCritChance()))
        print ("Armor: {:.2%}".format(self.getArmorReduce()))

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
    """Enemy object"""
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
    """Player object"""
    def __init__(self, playername):
        Character.__init__(self)
        self.name = playername
        self.level = 1
        self.gold = 0
        self.exp = 0
        self.exp_needed = 1000
        self.stat_list = [10, 10, 10, 10]
        self.equipment_stat_list = [0, 0, 0, 0]
        self.inventory = []
        self.armor = {"Helm": None, "Coat": None, "Gloves": None,
                      "Leggings": None, "Boots": None}
        self.weapons = {"Right Hand": items.Sword("Rusty Sword", [0, 0, 0, 0])}
        self.health = self.getMaxHealth()

    def giveExp(self, exp_earned):
        """Gives the player exp_earned experience and checks for level up"""
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
            print("You do not have enough gold!")
            return False
        else:
            self.gold -= gold_taken
            print(self.name + " lost " + repr(gold_taken) + " gold!")
            return True
    def deathGold(self, gold_taken=0):
        if ((self.gold < gold_taken)):
            self.gold -= self.gold
        else:
            self.gold -= gold_taken

    def giveItem(self, item):
        """Checks to see if inventory has space and gives item to player"""
        if len(self.inventory) <= 10:
            print(self.name + " recieved a " + item.name + "!")
            self.inventory.append(item)
        else:
            print("Inventory is full!")
            self.swapItem(item)
            # We need to offer player a choice to replace or discard. This might work with a new swapItem method added above. Not finished yet
    def swapItem(self, item):
        while True:
            print("Would you like to destroy an item out for " + item.name + "?")
            # try:
            if (input("\nSelection: \n(Y)es\n(N)o\n")) == "y":
                choice = 0
                # except ValueError:
                #    continue
            else:
                choice = 1
            if choice == 0:
                self.getInventory(self)
                self.giveItem(item)
                # if len(self.inventory) <= 10:
                #    print(self.name + " recieved a " + item.name + "!")
                #    self.inventory.append(item)
                break
            elif choice == 1:
                print(item.name + " was left behind.")
                break
            else:
                continue  # need to check what this would do
                # this would ask yes or no, if no is selected it exits. if yes is selected it lets you open inventory and destroy an item
                # self.giveItem(self,item)  if decided yes to destory and item and there is inventory space, then give the item again

    def getInventory(self, accessed_from="zone"):
        """Displays inventory and options"""
        if len(self.inventory) == 0:
            input("Your inventory is empty.\n" +
                      "Press enter to continue...")
            return

        while True:
            # Clearers should be removed from game.py if they're called here.
            os.system("cls" if os.name == "nt" else "clear")
            if len(self.inventory) == 1:
                print ("You are carrying {} item.\n".format(len(self.inventory)))
            else:
                print("You are carrying " \
                       "{} items.\n".format(len(self.inventory)))
            print("Inventory:")
            for i, x in enumerate(self.inventory):
                print ("{}) {}".format(i + 1, x.getName()))
            print ("{}) Exit".format(i + 2))
            try:
                choice = int(input("\nSelection: ")) - 1
            except ValueError:
                continue
            if choice <= i and choice >= 0:
                os.system("cls" if os.name == "nt" else "clear")
                option = self.inventory[choice].getOptions(accessed_from)

                if option == "equip":
                    if isinstance(self.inventory[choice], items.Armor):
                        self.equip(self.inventory[choice],
                                   self.armor,
                                   accessed_from)
                    elif isinstance(self.inventory[choice], items.Weapon):
                        self.equip(self.inventory[choice],
                                   self.weapons,
                                   accessed_from)
                    else:
                        print ("Type Check Error")
                    self.updateEquipmentStats()
                    break
                elif option == "consume":
                    self.inventory[choice].use(self)
                    self.inventory[choice].stack_size -= 1
                    if self.inventory[choice].stack_size == 0:
                        self.inventory.pop(choice)                        
                    input("Press \"Enter\" to continue...")
                    break
                elif option == "compare":
                    if isinstance(self.inventory[choice], items.Armor):
                        if self.armor.get(
                           self.inventory[choice].slot) is not None:
                            self.compareEquip(self.inventory[choice],
                                                  self.armor.get(
                                                  self.inventory[choice].slot),
                                              accessed_from)
                        else:
                            print ("No existing item to compare!")
                            input("Press \"Enter\" to continue...")
                    elif isinstance(self.inventory[choice], items.Weapon):
                        if self.weapons.get(
                           self.inventory[choice].slot) is not None:
                            self.compareEquip(self.inventory[choice],
                                 self.weapons.get(self.inventory[choice].slot),
                                 accessed_from)
                        else:
                            print ("No existing item to compare!")
                            input("Press \"Enter\" to continue...")
                    self.updateEquipmentStats()

                elif option == "destroy":
                    self.inventory.pop(choice)

            elif choice == i + 1:
                break
            else:
                continue

    def attack(self, receiver):
        self.weapons.get("Right Hand").attack(self, receiver)

    def equip(self, new_equipment, type_dict, accessed_from="zone"):
        if type_dict.get(new_equipment.slot) is not None:
            self.compareEquip(new_equipment, type_dict.get(new_equipment.slot))
        else:
            type_dict[new_equipment.slot] = self.inventory.pop(self.inventory.index(new_equipment))
            if accessed_from == "combat":
                self.status.append("skip")

    def compareEquip(self, new_equipment, cur_equipment, accessed_from="zone"):
        """Compares attributes of existing item with a new item"""
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            STAT_WIDTH = 12
            CUR_NAME_WIDTH = len(cur_equipment.name) + 2
            NEW_NAME_WIDTH = len(new_equipment.name) + 2
            WIDTH = 4
            print ("".join(("Stat".ljust(STAT_WIDTH),
                           "New".ljust(NEW_NAME_WIDTH),
                           "Current".ljust(CUR_NAME_WIDTH),
                           "Difference".ljust(WIDTH))))

            print ("".join(("Name".ljust(STAT_WIDTH),
                           new_equipment.name.ljust(NEW_NAME_WIDTH),
                           cur_equipment.name.ljust(CUR_NAME_WIDTH))))

            print ("".join(("Power".ljust(STAT_WIDTH),
                           str(new_equipment.stats[0]).ljust(NEW_NAME_WIDTH),
                           str(cur_equipment.stats[0]).ljust(CUR_NAME_WIDTH),
                           str(new_equipment.stats[0] - cur_equipment.stats[0]).ljust(WIDTH))))

            print ("".join(("Precision".ljust(STAT_WIDTH),
                           str(new_equipment.stats[1]).ljust(NEW_NAME_WIDTH),
                           str(cur_equipment.stats[1]).ljust(CUR_NAME_WIDTH),
                           str(new_equipment.stats[1] - cur_equipment.stats[1]).ljust(WIDTH))))

            print ("".join(("Toughness".ljust(STAT_WIDTH),
                           str(new_equipment.stats[2]).ljust(NEW_NAME_WIDTH),
                           str(cur_equipment.stats[2]).ljust(CUR_NAME_WIDTH),
                           str(new_equipment.stats[2] - cur_equipment.stats[2]).ljust(WIDTH))))

            print ("".join(("Vitality".ljust(STAT_WIDTH),
                           str(new_equipment.stats[3]).ljust(NEW_NAME_WIDTH),
                           str(cur_equipment.stats[3]).ljust(CUR_NAME_WIDTH),
                           str(new_equipment.stats[3] - cur_equipment.stats[3]).ljust(WIDTH))))
            choice = input("\nEquip " + new_equipment.name + "? (Y/N)").lower()
            if choice == 'y':
                if isinstance(new_equipment, items.Armor):
                    self.armor[new_equipment.slot] = self.inventory \
                                                .pop(self.inventory.index(new_equipment))
                elif isinstance(new_equipment, items.Weapon):
                    self.weapons[new_equipment.slot] = self.inventory \
                                              .pop(self.inventory.index(new_equipment))
                if accessed_from == "combat":
                    self.status.append("skip")
                break
            elif choice == 'n':
                os.system("cls" if os.name == "nt" else "clear")
                break

    def updateEquipmentStats(self):
        """Updates equipment stats after changing equipment"""
        for i in range(len(self.equipment_stat_list)):
            tmp_amount = 0
            for x in self.armor.values():
                if x is not None:
                    tmp_amount += x.stats[i]
                else:
                    tmp_amount += 0
            for x in self.weapons.values():
                if x is not None:
                    tmp_amount += x.stats[i]
                else:
                    tmp_amount += 0
            self.equipment_stat_list[i] = tmp_amount

    def checkLevelUp(self):
        """Checks to see if enough experience has been gained to level up"""
        level_gain = 0
        while self.exp >= self.exp_needed:
            print ("\nLevel up!!!")
            self.level += 1
            self.exp -= self.exp_needed
            self.exp_needed += self.level * 100
            level_gain += 1
        if level_gain > 0:
            input("Press \"Enter\" to continue...")
            os.system("cls" if os.name == "nt" else "clear")
            self.levelUp(level_gain)

    def levelUp(self, level_gain):
        """Allocate points to attributes"""
        points_gain = level_gain * 5
        while points_gain != 0:

            print ("Points available: ", points_gain)
            print ("[------------------]")
            print ("(1) Power: ", self.stat_list[0])
            print ("(2) Precision: ", self.stat_list[1])
            print ("(3) Toughness: ", self.stat_list[2])
            print ("(4) Vitality: ", self.stat_list[3])
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
        print ("[---Character Sheet---]")
        print ("Name: %s (Level: %d)" % (self.name, self.level))
        print ("Health: %d/%d" % (self.health, self.getMaxHealth()))
        print ("Gold: %d" % (self.gold))
        print ("Exp: %d/%d" % (self.exp, self.exp_needed))
        print ("\nPower: {} (+{})".format(self.stat_list[0] +
                                         self.equipment_stat_list[0],
                                         self.equipment_stat_list[0]))
        print ("Precision: {} (+{})".format(self.equipment_stat_list[1],
                                           self.equipment_stat_list[1]))
        print ("Toughness: {} (+{})".format(self.stat_list[2] +
                                           self.equipment_stat_list[2],
                                           self.equipment_stat_list[2]))
        print ("Vitality: {} (+{})".format(self.stat_list[3] +
                                          self.equipment_stat_list[3],
                                          self.equipment_stat_list[3]))
        print ("\nAttack: %d" % (self.getAttackDamage()))
        print ("Crit Chance: {:.2%}".format(self.getCritChance()))
        print ("Armor: {:.2%}".format(self.getArmorReduce()))

        print ("\n[------Equipment-----]")
        for x in self.armor:
            if self.armor.get(x) != None:
                name = self.armor.get(x).name
            else:
                name = "None"
            print ("{}: {}".format(x, name))

        print ("")
        for x in self.weapons:
            if self.weapons.get(x) is not None:
                name = self.weapons.get(x).name
            else:
                name = "None"
            print ("{}: {}".format(x, name))

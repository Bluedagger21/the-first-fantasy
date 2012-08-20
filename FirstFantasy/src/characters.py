'''
Last changed by: Dale Everett
'''
from weightedchoice import weighted_choice_sub
from random import random
import items
import os

class Character:
    """Base class"""
    def __init__(self):
        self.status = "normal"
        self.VITALITY_RATIO = 5
        self.POWER_RATIO = 1.5
        self.name = ""
        self.health = 5
        self.stat_list = [5,7,7,5]
        self.equipment_stat_list = [0,0,0,0]
        self.level = 1
    
    def getMaxHealth(self):
        return (self.stat_list[3]+self.equipment_stat_list[3]) * self.VITALITY_RATIO

    def getCritChance(self):
        return (0.1 * ((self.stat_list[1]+self.equipment_stat_list[1]) / ((self.level * 2.0) + 8.0)))

    def getArmorReduce(self):
        return (0.1 * ((self.stat_list[2]+self.equipment_stat_list[2]) / ((self.level * 3.0) + 7.0)))

    def getAttackDamage(self):
        return (self.stat_list[0]+self.equipment_stat_list[0]) * self.POWER_RATIO

    def getCharacterSheet(self):
        print "[---Character Sheet---]"
        print "Name: %s (Level: %d)" %(self.name,self.level)
        print "Health: %d/%d" %(self.health,self.getMaxHealth())
        print "\nPower: %d" %(self.stat_list[0])
        print "Precision: %d" %(self.stat_list[1])
        print "Toughness: %d" %(self.stat_list[2])
        print "Vitality: %d" %(self.stat_list[3])
        print "\nAttack: %d" %(self.getAttackDamage())
        print "Crit Chance: {0:.2f}%".format(100 * self.getCritChance())
        print "Armor: {0:.2f}%".format(100 * self.getArmorReduce())

    def attack(self,receiver):
        damage = self.getDamage()
        receiver.takeDamage(damage)
        print self.name + " attacked for " + repr(damage) + " (-{})".format(round(damage * receiver.getArmorReduce()))

    def takeDamage(self,damage):
        damage -= round(damage * self.getArmorReduce())
        self.health -= round(damage)
        if self.health <= 0:
            self.status = "dead"
            self.health = 0

    def getDamage(self):
        damage = self.getAttackDamage()
        if random() <= self.getCritChance():
            print "CRITICAL STRIKE!!!"
            damage *= 2
        return round(damage)

class Enemy(Character):
    """Enemy object"""
    def __init__(self,name,stats,level):
        Character.__init__(self)
        self.name = name
        self.level = level
        self.stat_weights = stats
        self.initLevel(level*5)
        self.health = self.getMaxHealth()

    def initLevel(self,level):
        for _ in range(level - 1):
            tmp_index = weighted_choice_sub(self.stat_weights)
            self.stat_list[tmp_index] += 1

class Player(Character):
    """Player object"""
    def __init__(self,playername):
        Character.__init__(self)
        self.name = playername
        self.level = 1
        self.gold = 0
        self.exp = 0
        self.exp_needed = 1000
        self.stat_list = [10,10,10,10]
        self.equipment_stat_list = [0,0,0,0]
        self.inventory = []
        self.armor = {"Helm":None, "Coat":None, "Gloves":None, "Leggings":None, "Boots":None}
        self.weapons = {"Right Hand":items.Sword("Rusty Sword",[0,0,0,0])}
        self.health = self.getMaxHealth()
    
    def giveExp(self,exp_earned):
        print self.name + " gained " + repr(exp_earned) + " experience!"
        self.exp += exp_earned
        self.checkLevelUp()

    def giveGold(self,gold_earned):
        print self.name + " gained " + repr(gold_earned) + " gold!"
        self.gold += gold_earned
        
    def giveItem(self,item):
        print self.name + " found a " + item.name + "!"
        if len(self.inventory) < 10:
            self.inventory.append(item)
        else:
            print "Inventory is full!"
    
    def getInventory(self):
        """Displays inventory and options"""
        if len(self.inventory) == 0:
            print "Your inventory is empty..."
            return
        while True:
            os.system("CLS")
            print "Inventory:"
            for i,x in enumerate(self.inventory):
                print "{}) {}".format(i+1,x.name)
            print "{}) Exit".format(i+2)
            try:
                choice = int(raw_input("\nSelection: ")) - 1
            except ValueError:
                continue
            if choice <= i and choice >= 0:
                os.system("CLS")
                option = self.inventory[choice].getOptions()
                
                if option == "equip":
                    tmp_slot = self.inventory[choice].slot
                    if isinstance(self.inventory[choice],items.Armor):
                        if self.armor.get(self.inventory[choice].slot) != None:
                            self.compareEquipment(self.inventory[choice], self.armor.get(self.inventory[choice].slot))
                        else:
                            self.armor[tmp_slot] = self.inventory.pop(choice)
                            
                    elif isinstance(self.inventory[choice],items.Weapon):
                        if self.weapons.get(self.inventory[choice].slot) != None:
                            self.compareEquipment(self.inventory[choice], self.weapons.get(self.inventory[choice].slot))
                        else:
                            self.weapons[tmp_slot] = self.inventory.pop(choice)
                     
                    else:
                        print "Type Check Error"
                               
                    self.updateEquipmentStats()
                    break
                
                elif option == "consume":
                    self.inventory.pop(choice).use(self)
                    os.system("PAUSE")
                    break
                
                elif option == "compare":
                    if isinstance(self.inventory[choice],items.Armor):
                        if self.armor.get(self.inventory[choice].slot) != None:
                            self.compareEquipment(self.inventory[choice], self.armor.get(self.inventory[choice].slot))
                            self.updateEquipmentStats()
                        else:
                            print "No existing item to compare!"
                            os.system("PAUSE")
                    elif isinstance(self.inventory[choice],items.Weapon):
                        if self.weapons.get(self.inventory[choice].slot) != None:
                            self.compareEquipment(self.inventory[choice], self.weapons.get(self.inventory[choice].slot))
                            self.updateEquipmentStats()
                        else:
                            print "No existing item to compare!"
                            os.system("PAUSE")
                            
                elif option == "destroy":
                    self.inventory.pop(choice)
                    
            elif choice == i+1:
                break
            else:
                continue
            
    def attack(self,receiver):
        self.weapons.get("Right Hand").attack(self,receiver)
        
                             
    def compareEquipment(self,new,cur):
        """Compares attributes of existing item with a new item"""
        while True:
            os.system("CLS")
            STAT_WIDTH = 12
            CUR_NAME_WIDTH = len(cur.name) + 2
            NEW_NAME_WIDTH = len(new.name) + 2
            WIDTH = 4
            print "".join(("Stat".ljust(STAT_WIDTH), "New".ljust(NEW_NAME_WIDTH), "Current".ljust(CUR_NAME_WIDTH), "Difference".ljust(WIDTH)))
            print "".join(("Name".ljust(STAT_WIDTH), new.name.ljust(NEW_NAME_WIDTH), cur.name.ljust(CUR_NAME_WIDTH)))
            print "".join(("Power".ljust(STAT_WIDTH), str(new.stats[0]).ljust(NEW_NAME_WIDTH), str(cur.stats[0]).ljust(CUR_NAME_WIDTH), str(new.stats[0] - cur.stats[0]).ljust(WIDTH)))
            print "".join(("Precision".ljust(STAT_WIDTH), str(new.stats[1]).ljust(NEW_NAME_WIDTH), str(cur.stats[1]).ljust(CUR_NAME_WIDTH), str(new.stats[1] - cur.stats[1]).ljust(WIDTH)))
            print "".join(("Toughness".ljust(STAT_WIDTH), str(new.stats[2]).ljust(NEW_NAME_WIDTH), str(cur.stats[2]).ljust(CUR_NAME_WIDTH), str(new.stats[2] - cur.stats[2]).ljust(WIDTH)))
            print "".join(("Vitality".ljust(STAT_WIDTH), str(new.stats[3]).ljust(NEW_NAME_WIDTH), str(cur.stats[3]).ljust(CUR_NAME_WIDTH), str(new.stats[3] - cur.stats[3]).ljust(WIDTH)))
            choice = raw_input("\nEquip " + new.name + "? (Y/N)").lower()
            if choice == 'y':
                if isinstance(new, items.Armor):
                    self.armor[new.slot] = new
                elif isinstance(new, items.Weapon):
                    self.weapons[new.slot] = new
                self.inventory.remove(new)
                os.system("CLS")
                break
            elif choice == 'n':
                os.system("CLS")
                break
    
    def updateEquipmentStats(self):
        """Updates equipment stats after changing equipment"""
        for i in range(len(self.equipment_stat_list)):
            tmp_amount = 0
            for x in self.armor.itervalues():
                if x != None:
                    tmp_amount += x.stats[i]
                else:
                    tmp_amount += 0
            for x in self.weapons.itervalues():
                if x != None:
                    tmp_amount += x.stats[i]
                else:
                    tmp_amount += 0
            self.equipment_stat_list[i] = tmp_amount

    def checkLevelUp(self):
        """Checks to see if enough experience has been gained to level up"""
        level_gain = 0
        while self.exp >= self.exp_needed:
            print "\nLevel up!!!"
            self.level += 1
            self.exp -= self.exp_needed
            self.exp_needed += self.level * 100
            level_gain += 1
        if level_gain > 0:
            os.system("PAUSE")
            os.system("CLS")
            self.levelUp(level_gain)
    
    def levelUp(self,level_gain):
        """Allocate points to attributes"""
        points_gain = level_gain * 5
        while points_gain != 0:
            
            print "Points available: ", points_gain
            print "[------------------]"
            print "(1) Power: ", self.stat_list[0]
            print "(2) Precision: ", self.stat_list[1]
            print "(3) Toughness: ", self.stat_list[2]
            print "(4) Vitality: ", self.stat_list[3]
            choice = raw_input("Place point into: ")
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
                os.system("CLS")
            points_gain -= 1
            self.health = self.getMaxHealth()
            os.system("CLS")

    def getCharacterSheet(self):
        print "[---Character Sheet---]"
        print "Name: %s (Level: %d)" %(self.name,self.level)
        print "Health: %d/%d" %(self.health,self.getMaxHealth())
        print "Gold: %d" %(self.gold)
        print "Exp: %d/%d" %(self.exp,self.exp_needed)
        print "\nPower: {} (+{})".format(self.stat_list[0]+self.equipment_stat_list[0],self.equipment_stat_list[0])
        print "Precision: {} (+{})".format(self.stat_list[1]+self.equipment_stat_list[1],self.equipment_stat_list[1])
        print "Toughness: {} (+{})".format(self.stat_list[2]+self.equipment_stat_list[2],self.equipment_stat_list[2])
        print "Vitality: {} (+{})".format(self.stat_list[3]+self.equipment_stat_list[3],self.equipment_stat_list[3])
        print "\nAttack: %d" %(self.getAttackDamage())
        print "Crit Chance: {0:.2f}%".format(100 * self.getCritChance())
        print "Armor: {0:.2f}%".format(100 * self.getArmorReduce())
        
        print "\n[------Equipment-----]"
        for x in self.armor.iterkeys():
            if self.armor.get(x) != None:
                name = self.armor.get(x).name
            else:
                name = "None"
            print "{}: {}".format(x,name)
        
        print ""
        for x in self.weapons.iterkeys():
            if self.weapons.get(x) != None:
                name = self.weapons.get(x).name
            else:
                name = "None"
            print "{}: {}".format(x,name)
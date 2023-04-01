import characters
import random
import inventory
import loottable
from status import *

class Enemy(characters.Character):
    # Enemy object
    def __init__(self, 
                 name, 
                 level, 
                 stats = None):
        super().__init__(name, stats, level)
        self.stats["Vitality"] = round(5*(1+0.1)**self.level)
        self.stats["Power"] = round(5*(1+0.1)**self.level)
        self.stats["Base Damage"] = round(5*(1+0.1)**self.level)
        self.stats["Crit"] = round(5*(1+0.1)**self.level)
        self.stats["Physical Resist"] = round(20*(1+0.1)**self.level)
        self.stats["Magical Resist"] = round(10*(1+0.1)**self.level)
        self.health = self.getMaxHealth()
        self.loot_table = loottable.LootGenerator(level, self)

class Spider(Enemy):
    def __init__(self, level, name="Spider"):
        self.stats={"Vitality": 5,
                    "Power": 5,
                    "Base Damage": 5,
                    "Crit": 5,
                    "Crit Multiplier": 1.5,
                    "Physical Resist": 15,
                    "Magical Resist" : 15}
        super().__init__(name, level, self.stats)
        self.actions = ["Bite", "Poison", "Web"]
        self.action_weights = [10, 2, 2]

    def attack(self, target: characters.Player):
        choice = random.choices(self.actions, weights=self.action_weights)[0]
        if choice == "Bite":
            potency = 1.0
            damage = self.getCalculatedDamage(target, potency)
            print("The Spider bites you for {} damage!".format(damage["Total Damage"]))
            target.takeDamage(damage["Total Damage"], self)

        elif choice == "Poison":
            target.status_list.append(Poison("Venom", self, target))
            print("The Spider poisons you!")

        elif choice == "Web":
            target.status_list.append(StatMod("Web", target, duration=3, stat_mod_dict={"Power": -self.stats["Power"]}))
            target.updateStats()
            print("The Spider entangles you in a web!")

class Thief(Enemy):
    def __init__(self, level, name="Thief"):
        self.stats={"Vitality": 5,
                    "Power": 5,
                    "Base Damage": 5,
                    "Crit": 5,
                    "Crit Multiplier": 1.5,
                    "Physical Resist": 20,
                    "Magical Resist" : 10}
        super().__init__(name, level, self.stats)
        self.actions = ["Stab", "Hide in Shadows", "Pickpocket"]
        self.action_weights = [10, 2, 2]

    def attack(self, target):
        choice = random.choices(self.actions, weights=self.action_weights)[0]
        if choice == "Stab":
            potency = 1.0
            damage = self.getCalculatedDamage(target, potency)
            print("The Thief stabs you for {} damage!".format(damage["Total Damage"]))
            target.takeDamage(damage["Total Damage"], self)

        elif choice == "Hide in Shadows":
            self.status_list.append(Status("Hide in Shadows", self, duration=3, phase="BoT"))
            print("The Thief creates a swirling mass of shadows around them!")

        elif choice == "Pickpocket":
            if len(target.inventory.item_list) == 0:
                print("The Thief fails to pickpocket from you as you have no items to steal!")
                self.item_stolen = None
            else:
                self.item_stolen = random.choice(target.inventory.item_list)
                target.inventory.remove(self.item_stolen)
                self.loot_table.loot_list.append(self.item_stolen)

                print("The Thief stole a {} from you!".format(self.item_stolen.name))

            if random.random() >= .5:
                potency = .5
                damage = self.getCalculatedDamage(target, potency, crit=False)
                print("The Thief also deals {} damage to you!".format(damage["Total Damage"]))

                target.takeDamage(damage["Total Damage"], self)

            




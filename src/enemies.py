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
        self.stats["Vitality"] = round(stats["Vitality"]*(1+0.15)**self.level)
        self.stats["Power"] = round(stats["Power"]*(1+0.1)**self.level)
        self.stats["Base Damage"] = round(stats["Base Damage"]*(1+0.1)**self.level)
        self.stats["Crit"] = round(stats["Crit"]*(1+0.1)**self.level)
        self.stats["Physical Resist"] = round(stats["Physical Resist"]*(1+0.1)**self.level)
        self.stats["Magical Resist"] = round(stats["Magical Resist"]*(1+0.1)**self.level)
        self.base_stats = stats
        self.health = self.getMaxHealth()
        self.loot_table = loottable.LootGenerator(level, self)

    def updateStats(self):
        self.stats.update(self.base_stats)
        
        new_status_stats = {}
        find_status = StatMod(None,None,None,None)
        status_stat_list = self.status_list.get(find_status)
        
        if len(status_stat_list) > 0:
            for status_i in status_stat_list:
                for stat_name in status_i.stat_mods:
                    if stat_name in new_status_stats:
                        new_status_stats[stat_name] += status_i.stat_mods[stat_name]
                    else:
                        new_status_stats.update({stat_name: status_i.stat_mods[stat_name]})

        for stat_name in new_status_stats:
            if stat_name in self.stats:
                self.stats[stat_name] += new_status_stats[stat_name]

class Spider(Enemy):
    def __init__(self, level, name="Spider"):
        self.stats={"Vitality": 3,
                    "Power": 3,
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
        self.stats={"Vitality": 10,
                    "Power": 3,
                    "Base Damage": 3,
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
            self.status_list.append(Status("Hide in Shadows", self, self, duration=3, phase="BoT"))
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

            




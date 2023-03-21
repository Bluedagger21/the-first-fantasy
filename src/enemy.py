import characters
import random
import inventory
import loottable

class Enemy(characters.Character):
    # Enemy object
    def __init__(self, 
                 name, 
                 level, 
                 stats = None):
        super().__init__(name, stats, level)
        self.update()
        self.health = self.getMaxHealth()
        self.loot_table = loottable.LootGenerator(level, self)

class Thief(Enemy):
    def __init__(self, name, level, stats=None):
        super().__init__(name, level, stats)
        self.actions = ["Stab", "Pickpocket"]
        self.action_weights = [10, 2]
        self.stats = {"Vitality": 20,
                      "Power": 10,
                      "Base Damage": 10,
                      "Crit": 5,
                      "Crit Multiplier": 1.5,
                      "Physical Resist": 20,
                      "Magical Resist" : 10}

    def attack(self, target):
        choice = random.choices(self.actions, weights=self.action_weights)[0]
        if choice == "Stab":
            damage = self.stats["Power"] + self.stats["Base Damage"]

            if random.random() <= self.stats["Crit"] / (100 + (5 * (target.level - 1))):
                print("CRITICAL STRIKE!!!")
                damage *= self.stats["Crit Multiplier"]

            calc_resist = .1 * ((20 * target.ilvl) / target.stats["Physical Resist"])
            round(damage - (damage * calc_resist))


            target.takeDamage(damage)

        elif choice == "Pickpocket":
            self.item_stolen = random.choice(target.inventory.item_list)
            target.inventory.remove(self.item_stolen)
            self.loot_table.loot_list.append(self.item_stolen)

            print("The Thief stole a {} from you!".format(self.item_stolen.name))

            if random.random >= .5:
                damage = self.stats["Power"] / 2
                calc_resist = .1 * ((20 * target.ilvl) / target.stats["Physical Resist"])
                round(damage - (damage * calc_resist))
                print("The Thief also deals {} damage to you!")

                target.takeDamage(damage)
            




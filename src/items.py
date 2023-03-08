import os
import random
class Equipment():
    # Base equippable item class
    def __init__(self, name, modifiers, stack_limit=1):
        self.name = name
        self.stack_limit = stack_limit
        self.stack_size = 1
        self.modifiers = modifiers
        self.attributes = {"Strength" : self.modifiers.setdefault("Strength", 0),
                           "Dexterity" : self.modifiers.setdefault("Dexterity", 0),
                           "Intelligence" : self.modifiers.setdefault("Intelligence", 0)}
        self.rarity = self.modifiers.setdefault("Rarity", "+0")

        if self.rarity != "+0":
            self.name += " {}".format(self.rarity)

    def getName(self):
        return self.name

    def showEverything(self):
        # Print attributes of the equipment
        print(self.name)
        print("STR: " + repr(self.attributes["Strength"]))
        print("DEX: " + repr(self.attributes["Dexterity"]))
        print("INT: " + repr(self.attributes["Intelligence"]))

    def getOptions(self, accessed_from="zone"):
        # Displays and prompts equipment options
        while True:
            self.showEverything()
            if accessed_from == "combat":
                print("\n*** Equipping This Item Will End Your Turn ***")
            print("\n(E)quip/Compare   (D)estroy    (Q)uit")
            choice = input("\nSelection: ").lower()
            if choice == 'e':
                return "equip"
            elif choice == 'd':
                return "destroy"
            elif choice == 'q':
                return "quit"
            # might need else continue here as well for input validation?
class Armor(Equipment):
    # Derived class from Equipment
    def __init__(self, name, slot, modifiers, stack_limit=1):
        super().__init__(name, modifiers, stack_limit)
        self.slot = slot

class Weapon(Equipment):
    # Derived class from Equipment
    def __init__(self, name, modifiers, slot="Main Hand", stack_limit=1):
        super().__init__(name, modifiers, stack_limit)
        self.slot = slot
        self.base_damage_total = self.modifiers.setdefault("Base Damage Total", 5)
        self.base_damage = self.modifiers.setdefault("Base Damage", 5)
        self.base_increase = self.modifiers.setdefault("Base Increase", 0)
        self.random_damage_total = self.modifiers.setdefault("Random Damage Total", 5)
        self.random_damage = self.modifiers.setdefault("Random Damage", 5)
        self.random_increase = self.modifiers.setdefault("Random Damage Increase", 0)
        self.random_mult = self.modifiers.setdefault("Random Multiplier", 1)
        self.base_crit_rate = self.modifiers.setdefault("Base Crit Rate", .05)
        self.crit_mult = self.modifiers.setdefault("Crit Multiplier", 2)

        if self.rarity == "+1":
            self.base_increase += 1
        elif self.rarity == "+2":
            self.base_increase += 2
        elif self.rarity == "+3":
            self.base_increase += 3
        elif self.rarity == "+4":
            self.base_increase += 4
        elif self.rarity == "+5":
            self.base_increase += 5

        self.base_damage_total = self.base_damage + self.base_increase
        self.modifiers.update({"Base Damage Total": self.base_damage_total})
        self.random_damage_total = self.random_damage + self.random_increase
        self.modifiers.update({"Random Damage Total": self.random_damage_total})

    def getCalculatedDamage(self, dealer):
        dealer_dmg_inc = dealer.attribute_bonuses["str_base_dmg"][2]
        dealer_rnd_dmg_inc = dealer.attribute_bonuses["dex_rnd_dmg"][2]

        calc_base_dmg = self.base_damage_total + dealer_dmg_inc
        rnd_dmg = 0
    
        for i in range(self.random_mult):
            rnd_dmg += random.randrange(self.random_damage_total + dealer_rnd_dmg_inc + 1)
        
        return calc_base_dmg + rnd_dmg

    def showEverything(self):
        # Print everything from the equipment
        print(self.name)
        print("STR: " + repr(self.attributes["Strength"]))
        print("DEX: " + repr(self.attributes["Dexterity"]))
        print("INT: " + repr(self.attributes["Intelligence"]))
        print("Attack: {} + {}d({})".format(self.base_damage_total, self.random_mult, self.random_damage_total))

class Consumable():
    # Defines base members and methods for consumables
    def __init__(self, stack_limit=5, stack_size=1):
        self.stack_limit = stack_limit
        self.stack_size = stack_size
        self.slot = "consumable"

    def getName(self):
        return self.name + " (" + str(self.stack_size) + "/" + str(self.stack_limit) + ")"

    def getOptions(self, accessed_from="zone"):
        # Display and prompt options
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            self.show()
            print("\n(U)se    (D)estroy    (Q)uit")
            try:
                choice = input("\nSelection: ").lower()
            except ValueError:
                continue
            if choice == 'u':
                return "consume"
            elif choice == 'd':
                return "destroy"
            elif choice == 'q':
                return "quit"



class SmallHealthPotion(Consumable):
    def __init__(self, stack_limit=5, stack_size=1):
        super().__init__(stack_limit, stack_size)
        self.name = "Small Health Potion"
        self.effect = "Effect: Restores 20 health"
        

    def use(self, target):
        print(target.name + " used a " + self.name + ".")
        target.giveHealth(20)
        print(target.name + " gained 20 health! ({}/{})".format(
                                          target.health, 
                                          target.getMaxHealth()))
    
    def show(self):
        # Print name and effect
        print(self.getName())
        print(self.effect)

class SmallExperienceBoost(Consumable):
    def __init__(self, stack_limit=5, stack_size=1):
        super().__init__(stack_limit, stack_size)
        self.name = "Small Experience Boost"
        self.effect = "Effect: Grants 100 experience"

    def use(self, target):
        print(target.name + " used a " + self.name + ".")
        target.giveExp(100)
    
    def show(self):
        # Print name and effect
        print(self.getName())
        print(self.effect)

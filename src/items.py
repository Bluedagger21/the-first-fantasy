import os
import random
class Equipment():
    # Base equippable item class
    def __init__(self, name, modifiers, stack_limit = 1):
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

    def show(self):
        # Print attributes of the equipment
        print(self.name)
        print("STR: " + repr(self.attributes["Strength"]))
        print("DEX: " + repr(self.attributes["Dexterity"]))
        print("INT: " + repr(self.attributes["Intelligence"]))

    def getOptions(self, accessed_from="zone"):
        # Displays and prompts equipment options
        while True:
            self.show()
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
class Armor(Equipment):
    # Derived class from Equipment
    def __init__(self, name, modifiers, slot, stack_limit=1):
        super().__init__(name, modifiers, stack_limit )
        self.slot = slot

class Weapon(Equipment):
    # Derived class from Equipment
    def __init__(self, name, modifiers, slot = "Main Hand", stack_limit=1):
        super().__init__(name, modifiers, stack_limit)
        self.slot = slot
        self.base_damage = modifiers.setdefault("Base Damage", 5)
        self.base_increase = modifiers.setdefault("Base Increase", 0)
        self.random_damage = modifiers.setdefault("Random Damage", 5)
        self.random_increase = modifiers.setdefault("Random Damage Increase", 0)
        self.random_mult = modifiers.setdefault("Random Multiplier", 1)
        self.base_crit_rate = modifiers.setdefault("Base Crit Rate", .05)
        self.crit_mult = modifiers.setdefault("Crit Multiplier", 2)

        if self.rarity is "+1":
            self.base_increase += 1
        elif self.rarity is "+2":
            self.base_increase += 2
        elif self.rarity is "+3":
            self.base_increase += 3
        elif self.rarity is "+4":
            self.base_increase += 4
        elif self.rarity is "+5":
            self.base_increase += 5

    def getCalculatedDamage(self, dealer):
        base_dmg_inc = (1 + (self.base_increase/1))
        rnd_dmg_inc = (1 + (self.random_increase/1))

        base_dmg = self.base_damage + base_dmg_inc
        rnd_dmg = 0
    
        for i in range(self.random_mult):
            rnd_dmg += random.randrange(self.random_damage + rnd_dmg_inc)
        
        return base_dmg + rnd_dmg

class Consumable():
    # Defines base members and methods for consumables
    def __init__(self, name, effect, stack_limit = 5, stack_size = 1):
        self.name = name
        self.effect = effect
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

    def show(self):
        # Print name and effect
        print(self.getName())
        print(self.effect)

class SmallHealthPotion(Consumable):
    def __init__(self):
        self.name = "Small Health Potion"
        self.effect = "Effect: Restores 20 health"
        Consumable.__init__(self, self.name, self.effect)

    def use(self, target):
        print(target.name + " used a " + self.name + ".")
        target.giveHealth(20)
        print(target.name + " gained 20 health! ({}/{})".format(
                                          target.health, 
                                          target.getMaxHealth()))

class SmallExperienceBoost(Consumable):
    def __init__(self):
        self.name = "Small Experience Boost"
        self.effect = "Effect: Grants 100 experience"
        Consumable.__init__(self, self.name, self.effect)

    def use(self, target):
        print(target.name + " used a " + self.name + ".")
        target.giveExp(100)
import items
import random
from weightedchoice import weighted_choice_sub

class LootGenerator:
    def __init__(self, ilvl, owner):
        self.ilvl = ilvl
        self.owner = owner

        self.rarity_weights = [200, 40, 20, 10, 5, 1]
        self.rarity_scales = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
        self.rarity = [0, 1, 2, 3, 4, 5]

        self.item_types = {"Consumable": {"Subtypes": ("SmallXP",
                                                       "SmallHP"),
                                          "Subtype Weights": [1, 3],
                                          "Type Weight": 25},
                           "Equipment": {"Subtypes": ("Weapon",
                                                      "Armor"),
                                         "Subtype Weights": [2, 6],
                                         "Type Weight": 45},
                           "Unique": {"Type Weight": 0},
                           "None": {"Type Weight": 29}}

        self.weapon_list = [items.Sword, items.Staff, items.Dagger, items.Wand]
        self.armor_dict = {"Head": {"Helmet": {"Vitality": 5,
                                               "Physical Resist": 5,
                                               "Magical Resist": 5}},
                           "Body": {"Breastplate": {"Vitality": 5,
                                                    "Physical Resist": 5,
                                                    "Magical Resist": 5}},
                           "Hands": {"Gauntlets": {"Vitality": 5,
                                                   "Physical Resist": 5,
                                                   "Magical Resist": 5}},
                           "Feet": {"Greaves": {"Vitality": 5,
                                                "Physical Resist": 5,
                                                "Magical Resist": 5}}}
        self.unique_dict = {"Main Hand": {"Demonforged Blade": {"Base Damage": 5,
                                                                "Random Damage": 5},
                                          "Bane of Darkness": {"Base Damage": 6,
                                                               "Random Damage": 4},
                                          "Throatsplitter": {"Base Damage": 2,
                                                             "Random Damage": 4,
                                                             "Random Multiplier": 2,
                                                             "Crit Rate": 0.10,
                                                             "Crit Multiplier": 3}},
                            "Head": {"Sanctuary": {"HP": 5,
                                                   "Physical Resist": .01},
                                     "Thorned Crown": {"HP": 3,
                                                       "Evasion": .01}},
                            "Body": {"Judgement's Chestguard": {"HP": 5,
                                                                "Physical Resist": .01},
                                     "Warrior's Wrappings": {"HP": 3,
                                                             "Evasion": .01}},
                            "Hands": {"Fierce Grip": {"HP": 5,
                                                      "Physical Resist": .01},
                                      "Leather Gloves": {"HP": 3,
                                                         "Evasion": .01}},
                            "Feet": {"Gravestompers": {"HP": 5,
                                                       "Physical Resist": .01},
                                     "Leather Boots": {"HP": 3,
                                                       "Evasion": .01}}}
        self.loot_list = []

    def generateLoot(self):

        self.loot_list.append(self.ilvl * random.randrange(8, 20))
        self.loot_list.append(self.generateItem())
        return self.loot_list

    def generateItem(self):
        generated_item = None
        item_type = self.determineItemType()
        item_rarity = self.determineRarity()
        item_quality = self.determineQuality()

        if item_type == "Consumable":
            generated_item = self.createConsumable()
        elif item_type == "Equipment":
            type_of_equipment = random.choices(self.item_types["Equipment"]["Subtypes"], weights=self.item_types["Equipment"]["Subtype Weights"])[0]
            if type_of_equipment == "Weapon":
                generated_item = self.createWeapon(self.ilvl, item_rarity, item_quality)
            elif type_of_equipment == "Armor":
                generated_item = self.createArmor(self.ilvl, item_rarity, item_quality)
        elif item_type == "Unique":
            generated_item = self.createUnique(self.ilvl, item_rarity, item_quality)
        return generated_item
            
    def determineItemType(self):
        list_of_items = list(self.item_types.items())
        weight_of_items = []

        for value in self.item_types.values():
            weight_of_items.append(value["Type Weight"])
        return random.choices(list_of_items, weights=weight_of_items)[0][0]

    def determineRarity(self):
        for i, x in enumerate(self.rarity):
            if i > self.ilvl:
                self.rarity_weights[i] = 0
            else:
                self.rarity_weights[i] = self.rarity_weights[i] * ((1 + self.ilvl) * self.rarity_scales[i])
        return random.choices(self.rarity, weights=self.rarity_weights)[0]
    
    def determineQuality(self):
        return round(100 * random.random())
        
    def createUnique(self, ilvl, rarity, quality):
        modifiers_dict = {"Rarity": rarity}
        created_item_slot = random.choices(list(self.unique_dict.keys()))[0]
        base_name, stats = random.choices(list(self.unique_dict[created_item_slot].items()))[0]

        modifiers_dict.update(stats)

        if created_item_slot == "Main Hand":
            return items.Weapon(base_name, modifiers_dict)
        else:
            return items.Armor(base_name, created_item_slot, modifiers_dict)

    def createConsumable(self):
        created_item_type = random.choices(self.item_types["Consumable"]["Subtypes"], weights=self.item_types["Consumable"]["Subtype Weights"])[0]
        if created_item_type == "SmallXP":
            return items.SmallExperienceBoost()
        elif created_item_type == "SmallHP":
            return items.SmallHealthPotion()
        return created_item_type()
    
    def createWeapon(self, ilvl, item_rarity, quality):
        weapon_type = random.choice(self.weapon_list)
        new_weapon = weapon_type(rarity=item_rarity, quality=quality, ilvl=ilvl)
        return new_weapon
        
    def createArmor(self, ilvl, item_rarity, quality):
        modifiers_dict = {}
        
        slot, base_dict = random.choice(list(self.armor_dict.items()))
        base_name, stats = random.choice(list(base_dict.items()))

        modifiers_dict.update(stats)
        
        return items.Armor(base_name, slot, modifiers_dict, ilvl, item_rarity, quality)
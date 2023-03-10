import items
import random
from weightedchoice import weighted_choice_sub

class LootGenerator:
    def __init__(self, ilvl, owner):
        self.ilvl = ilvl
        self.owner = owner

        self.rarity_weights = [200, 40, 20, 10, 5, 1]
        self.rarity_scales = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
        self.rarity = ["+0", "+1", "+2", "+3", "+4", "+5"]

        self.item_types = {"Consumable": {"Subtypes": ("SmallXP",
                                                       "SmallHP"),
                                          "Subtype Weights": [1, 2],
                                          "Type Weight": 25},

                           "Equipment": {"Subtypes": ("Weapon",
                                                      "Armor"),
                                         "Subtype Weights": [2, 8],
                                         "Type Weight": 35},
                           "Unique": {"Type Weight": 1},
                           "None": {"Type Weight": 39}
                          }
        
        self.weapon_dict = {"Sword": {"Base Damage": 5,
                                      "Random Damage": 5},
                            "Mace": {"Base Damage": 6,
                                     "Random Damage": 4},
                            "Dagger": {"Base Damage": 4,
                                       "Random Damage": 6}}
        self.armor_dict = {"Head": {"Helmet": {"Strength": 1,
                                               "Dexterity": 0},
                                    "Tricorn": {"Strength": 0,
                                                "Dexterity": 1}},
                           "Body": {"Breastplate": {"Strength": 1,
                                                    "Dexterity": 0},
                                    "Leather Wrappings": {"Strength": 0,
                                                          "Dexterity": 1}},
                           "Hands": {"Gauntlets": {"Strength": 1,
                                                   "Dexterity": 0},
                                     "Leather Gloves": {"Strength": 0,
                                                        "Dexterity": 1}},
                           "Feet": {"Greaves": {"Strength": 1,
                                                "Dexterity": 0},
                                    "Leather Boots": {"Strength": 0,
                                                      "Dexterity": 1}}}
        self.unique_dict = {"Main Hand": {"Demonforged Blade": {"Base Damage": 5,
                                                                "Random Damage": 5},
                                          "Bane of Darkness": {"Base Damage": 6,
                                                               "Random Damage": 4},
                                          "Throatsplitter": {"Base Damage": 2,
                                                             "Random Damage": 4,
                                                             "Random Multiplier": 2,
                                                             "Crit Rate": 0.10,
                                                             "Crit Multiplier": 3}},
                            "Head": {"Sanctuary": {"Strength": 1,
                                                   "Dexterity": 0},
                                     "Thorned Crown": {"Strength": 0,
                                                       "Dexterity": 1}},
                            "Body": {"Judgement's Chestguard": {"Strength": 1,
                                                                "Dexterity": 0},
                                     "Warrior's Wrappings": {"Strength": 0,
                                                             "Dexterity": 1}},
                            "Hands": {"Fierce Grip": {"Strength": 1,
                                                      "Dexterity": 0},
                                      "Leather Gloves": {"Strength": 0,
                                                         "Dexterity": 1}},
                            "Feet": {"Gravestompers": {"Strength": 1,
                                                       "Dexterity": 0},
                                     "Leather Boots": {"Strength": 0,
                                                       "Dexterity": 1}}}

        self.loot_list = []
    def generateLoot(self):
        self.loot_list.append(self.ilvl * random.randrange(8, 20))
        self.loot_list.append(self.generateItem())
        return self.loot_list

    def generateItem(self):
        generated_item = None
        item_type = self.determineItemType()
        item_rarity = self.determineRarity()

        if item_type == "Consumable":
            generated_item = self.createConsumable()
        elif item_type == "Equipment":
            type_of_equipment = random.choices(self.item_types["Equipment"]["Subtypes"], weights=self.item_types["Equipment"]["Subtype Weights"])[0]
            if type_of_equipment == "Weapon":
                generated_item = self.createWeapon(item_rarity)
            elif type_of_equipment == "Armor":
                generated_item = self.createArmor(item_rarity)
        elif item_type == "Unique":
            generated_item = self.createUnique(item_rarity)
        return generated_item
            

    def determineItemType(self):
        list_of_items = list(self.item_types.items())
        weight_of_items = []

        for value in self.item_types.values():
            weight_of_items.append(value["Type Weight"])
        return random.choices(list_of_items, weights=weight_of_items)[0][0]

    def determineRarity(self):
        for i,x in enumerate(self.rarity):
            if i > self.ilvl:
                self.rarity_weights[i] = 0
            else:
                self.rarity_weights[i] = self.rarity_weights[i] * ((1 + self.ilvl) * self.rarity_scales[i])
        return random.choices(self.rarity, weights=self.rarity_weights)[0]
        
    def createUnique(self, rarity):
        modifiers_dict = {"Rarity" : rarity}
        created_item_slot = random.choices(self.unique_dict.keys())[0]
        base_name, stats = random.choices(list(self.unique_dict[created_item_slot].items()))

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
    
    def createWeapon(self, item_rarity):
        modifiers_dict = {"Rarity": item_rarity,
                          "Strength": 0,
                          "Dexterity": 0,
                          "Intelligence": 0}
        base_name, stats = random.choice(list(self.weapon_dict.items()))
        
        modifiers_dict.update(stats)

        return items.Weapon(base_name, modifiers_dict)
        
    def createArmor(self, item_rarity):
        modifiers_dict = {"Rarity": item_rarity,
                          "Strength": 0,
                          "Dexterity": 0,
                          "Intelligence": 0}

        slot, base_dict = random.choice(list(self.armor_dict.items()))
        base_name, stats = random.choice(list(base_dict.items()))

        modifiers_dict.update(stats)
        # for modifier in list(stats.items()):
        #     modifiers_dict.update(modifier)
        
        return items.Armor(base_name, slot, modifiers_dict)
        
# def createUnique(quality):
#     # Chooses a unique item.
#     # Quality 0 armor have 8 stat points total.
#     # Quality 0 weapons have 12 stat points total.
#     unique_list = ((items.Sword("Demonforged Blade", [3, 3, 3, 3])),
#                    (items.Mace("Bane of Darkness", [3, 1, 5, 3])),
#                    (items.Dagger("Throatslitter", [3, 6, 1, 2])),
#                    (items.Armor("Judgement Chestguard", "Chest",
#                                 [3, 1, 3, 1])),
#                    (items.Armor("Warrior's Chestwraps", "Chest",
#                                 [6, 6, -2, -2])),
#                    (items.Armor("Sanctuary", "Helm", [0, 1, 4, 3])),
#                    (items.Armor("Thorned Crown", "Helm", [3, 3, 3, -1])),
#                    (items.Armor("Dragonhide Cloak", "Coat", [2, 1, 3, 2])),
#                    (items.Armor("Fiercegrip", "Gloves", [3, 2, 2, 1])),
#                    (items.Armor("Veracious Leggings", "Leggings",
#                                 [2, 3, 3, 0])),
#                    (items.Armor("Gravestompers", "Boots", [2, 2, 2, 2])))
#     return random.choice(unique_list)
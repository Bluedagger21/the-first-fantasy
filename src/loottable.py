import items
import random
from weightedchoice import weighted_choice_sub

class LootGenerator:
    def __init__(self, ilvl, owner):
        self.ilvl = ilvl
        self.owner = owner

        self.drop_types=["None", "Consumable", "Equipment"]
        self.drop_types_wieghts = [10, 10, 10]
        self.rarity_weights = [200, 40, 20, 10, 5, 1]
        self.rarity_scales = [1.0, 1.1, 1.2, 1.3, 1.4, 1.5]
        self.rarity = ["+0", "+1", "+2", "+3", "+4", "+5"]

        self.item_types = {"Consumable": ("SmallXP",
                                          "SmallHP"),
                           "Equipment": ("Weapon",
                                         "Armor")
                          }
        
        self.weapon_dict = {"Sword": {"Base Damage" : 5,
                                      "Random Damage" : 5},
                            "Mace": {"Base Damage" : 6,
                                     "Random Damage" : 4},
                            "Dagger": {"Base Damage" : 4,
                                       "Random Damage" : 6}}
        self.armor_dict = {"Helm": {"Helmet" : {"Strength" : 1,
                                                "Dexterity" : 0},
                                    "Tricorn" : {"Strength" : 0,
                                                 "Dexterity" : 1}},
                           "Body": {"Breastplate" : {"Strength" : 1,
                                                     "Dexterity" : 0},
                                    "Leather Wrappings" : {"Strength" : 0,
                                                           "Dexterity" : 1}},
                           "Hand": {"Gauntlets" : {"Strength" : 1,
                                                   "Dexterity" : 0},
                                    "Leather Gloves" : {"Strength" : 0,
                                                        "Dexterity" : 1}},
                           "Feet": {"Greaves" : {"Strength" : 1,
                                                 "Dexterity" : 0},
                                    "Leather Boots" : {"Strength" : 0,
                                                       "Dexterity" : 1}}}

        self.loot_list = []
    def generateLoot(self):
        self.loot_list.append(self.ilvl * random.randrange(8, 20))
        self.loot_list.append(self.generateItem())
        return self.loot_list

    def generateItem(self):
        generated_item = None
        item_type = self.determineItemType()
        item_rarity = self.determineRarity()

        if item_type is "Consumable":
            generated_item = self.createConsumable()
        elif item_type is "Equipment":
            type_of_equipment = random.choices(self.item_types["Equipment"], weights=[2,5])[0]
            if type_of_equipment is "Weapon":
                generated_item = self.createWeapon(item_rarity)
            elif type_of_equipment is "Armor":
                generated_item = self.createArmor(item_rarity)
        return generated_item
            

    def determineItemType(self):
        return random.choices(list(self.item_types.items()), weights=self.drop_types_wieghts)[0][0]

    def determineRarity(self):
        for i,x in enumerate(self.rarity):   
            self.rarity_weights[i] = self.rarity_weights[i] * ((1 + self.ilvl) * self.rarity_scales[i])
        return random.choices(self.rarity, weights=self.rarity_weights)[0]
        
    def createConsumable(self):
        created_item_type = random.choices(self.item_types["Consumable"], weights=[10,2])[0]
        if created_item_type == "SmallXP":
            return items.SmallExperienceBoost()
        elif created_item_type == "SmallHP":
            return items.SmallHealthPotion()
        return created_item_type()
    
    def createWeapon(self, item_rarity):
        modifiers_dict = {"Rarity" : item_rarity,
                          "Strength" : 0,
                          "Dexterity" : 0,
                          "Intelligence" : 0}
        base_name, stats = random.choice(list(self.weapon_dict.items()))
        
        modifiers_dict.update(stats)

        return items.Weapon(base_name, modifiers_dict)
        
    def createArmor(self, item_rarity):
        modifiers_dict = {"Rarity" : item_rarity,
                          "Strength" : 0,
                          "Dexterity" : 0,
                          "Intelligence" : 0}

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

# def loot(level):
#     # Decides loot given for the kill
#     gold = random.randint(0, 10) * level + 10
#     quality = level // 4
#     item_type_list = [("None", 2), ("Armor", 10), ("Weapon", 7),
#                       ("Consumable", 7), ("Rare", 1)]
#     item_type = item_type_list[weighted_choice_sub([x[1] for x
#                                                     in item_type_list])][0]
#     if item_type == "Consumable":
#         item = createConsumable(quality)
#     elif item_type == "Armor":
#         item = createArmor(quality)
#     elif item_type == "Weapon":
#         item = createWeapon(quality)
#     elif item_type == "Rare":
#         item = createUnique(quality)
#     else:
#         item = None
#     return (gold, item)

# armor_slots = ["Helm", "Coat", "Gloves", "Leggings", "Boots"]
# weapon_types = [("Sword", "Right Hand", [1, 0, 0, 0]),
#                 ("Mace", "Right Hand", [0, 0, 1, 0]),
#                 ("Dagger", "Right Hand", [0, 1, 0, 0])]
# weapon_prefixes = [("", 10, [0, 0, 0, 0]),
#                    ("Sharp ", 1, [1, 1, 0, 0]),
#                    ("Precise ", 1, [0, 1, 1, 0]),
#                    ("Stalwart ", 1, [0, 0, 1, 1]),
#                    ("Unyielding ", 1, [1, 0, 0, 1])]
# armor_prefixes = [("Crude ", [0, 0, 1, 0]),
#                   ("Basic ", [0, 0, 2, 0]),
#                   ("Sturdy ", [0, 0, 2, 1])]
# suffixes = [("", (10, [0, 0, 0, 0])),
#              (" of Brutality", (1, [1, 1, 0, 0])),
#              (" of Survival", (1, [0, 0, 1, 1])),
#              (" of Finesse", (1, [0, 1, 1, 0])),
#              (" of Dueling", (1, [1, 0, 0, 1]))]

# def createArmor(quality, armor_slot=""):
#     # Creates a piece of armor
#     stats = []

#     if armor_slot == "":
#         slot = random.choice(armor_slots)
#     else:
#         slot = armor_slot
#     prefix = armor_prefixes[quality]
#     suffix = suffixes[weighted_choice_sub([x[1][0] for x in suffixes])]
#     name = prefix[0] + slot + suffix[0]
#     for i in range(4):
#         stats.append(prefix[1][i] + suffix[1][1][i])
#     return items.Armor(name, slot, stats)

# def createWeapon(quality, weapon_type=""):
#     # Creates a weapon
#     stats = []
#     if weapon_type == "":
#         w_type = random.choice(weapon_types)
#     else:
#         w_type = weapon_type
#     prefix = weapon_prefixes[weighted_choice_sub(
#                             [x[1] for x in weapon_prefixes])]
#     name = prefix[0] + w_type[0]
#     for i in range(4):
#         stats.append((prefix[2][i] + w_type[2][i]) * (1 + quality))
#     if w_type[0] == "Sword":
#         return items.Sword(name, stats)
#     if w_type[0] == "Mace":
#         return items.Mace(name, stats)
#     if w_type[0] == "Dagger":
#         return items.Dagger(name, stats)

# def createConsumable(quality):
#     # Chooses a consumable
#     consumable_weights = (10, 2)
#     choice = weighted_choice_sub(consumable_weights)
#     if choice == 0:
#         return items.SmallHealthPotion()
#     elif choice == 1:
#         return items.SmallExperienceBoost()
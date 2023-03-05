import items
import os

class Storage:
    # Defines base members and methods for storing and accessing generic items
    def __init__(self, capacity, owner):
        self.capacity = capacity
        self.owner = owner
        self.item_list = []
        
    def length(self):
        return len(self.item_list)
    
    def isEmpty(self):
        return self.length() == 0
    
    def isFull(self):
        return self.length() >= self.capacity

    def add(self, item):
        # Is item stackable?
        if item.stack_limit > 1:
            # Determine if stackable item is already in item_list
            for i, x in enumerate(self.item_list):
                if x.name == item.name:
                    # Is there room in the stack?
                    if x.stack_size < x.stack_limit:
                        self.item_list[i].stack_size += 1
                        return True
        
        # Is item_list full?
        if self.isFull() is True:
            while True:
                print("\nInventory full!")
                print("What do you want to do with {}?".format(item.name))
                if(isinstance(item, items.Consumable)):
                    print("(R)eplace   (D)iscard    (U)se")
                else:
                    print("(R)eplace   (D)iscard")
                choice = input("\nSelection: ").lower()
                if choice == 'r':
                    item_to_remove = self.access()
                    if item_to_remove is False:
                        os.system("cls" if os.name == "nt" else "clear")
                        continue
                    else:
                        self.remove(item_to_remove)
                        self.add(item)
                        return True
                elif choice == 'd':
                    return False
                elif choice == 'u':
                    self.use(item, self.owner)
                    return False
        else:
            self.item_list.append(item)
            return True

    def remove(self, item, amount=1):
        for i, x in enumerate(self.item_list):
            if x == item:
                self.item_list[i].stack_size -= amount
                if x.stack_size <= 0:
                    self.item_list.pop(i)
    
    def use(self, item, target):
        while True:
            if item.stack_size > 1:
                try:
                    amount_to_use = int(input("How many? (Max: {}): ".format(item.stack_size)))
                except ValueError:
                    continue
            else:
                amount_to_use = 1
            if 0 < amount_to_use <= item.stack_size:
                while amount_to_use > 0:
                    item.use(target)
                    self.remove(item)
                    amount_to_use -= 1
                return
            else:
                continue        
    
    def access(self, from_where = "zone"):
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            print("Inventory:")
            for i, x in enumerate(self.item_list):
                print("{}) {}".format(i + 1, x.getName()))
            print("{}) Exit".format(i + 2))
            try:
                choice = int(input("\nSelection: "))
            except ValueError:
                continue
            if 0 <= (choice - 1) <= i:
                return self.item_list[choice - 1]
            else:
                return False
class Equipment():
    # Defines base members and methods for managing equipped items
    def __init__(self, owner):
        self.slots_dict = {"Head": None, 
                           "Body": None, 
                           "Hands": None,
                           "Feet": None,
                           "Main Hand": items.Weapon("Rusty Sword",
                                                      {"Base Damage" : 5, 
                                                       "Random Damage" : 5,
                                                       "Rarity" : "+0",
                                                       "Strength" : 0,
                                                       "Dexterity" : 0,
                                                       "Intelligence" : 0}),
                           "Off Hand": None}
        self.owner = owner
        self.total_attributes = self.updateAttributes()
    
    def getAttributes(self):
        return self.total_attributes

    def updateAttributes(self):
        self.total_attributes = {"Strength" : 0,
                                 "Dexterity" : 0,
                                 "Intelligence" : 0}
        for slot in self.slots_dict.values():
            if slot is None:
                continue
            else:
                self.total_attributes["Strength"] += slot.attributes.get("Strength", 0)
                self.total_attributes["Dexterity"] += slot.attributes.get("Dexterity", 0)
                self.total_attributes["Intelligence"] += slot.attributes.get("Intelligence", 0)
        return self.total_attributes
    
    def equip(self, new_equipment, inventory, accessed_from="zone"):
        slot = new_equipment.slot
        if self.slots_dict.get(slot) is not None:
            replaced_equipment = self.compareEquip(new_equipment, self.slots_dict.get(slot), slot)
            if replaced_equipment is False:
                return False
            if replaced_equipment is not None:
                inventory.remove(new_equipment)
                inventory.add(replaced_equipment)
        else:
            self.actuallyEquip(new_equipment, slot)
            inventory.remove(new_equipment)
        return True
    
    def actuallyEquip(self, new_equipment, slot):
        self.slots_dict[slot] = new_equipment
        self.updateAttributes()
    
    def compareEquip(self, new_equipment, cur_equipment, slot):
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            STAT_WIDTH = 12
            CUR_NAME_WIDTH = len(cur_equipment.name) + 2
            NEW_NAME_WIDTH = len(new_equipment.name) + 2
            DIF_WIDTH = len("Difference")
            print("".join(("Stat".ljust(STAT_WIDTH),
                           "New".ljust(NEW_NAME_WIDTH),
                           "Current".ljust(CUR_NAME_WIDTH),
                           "Difference".ljust(DIF_WIDTH))))

            print("-"*(STAT_WIDTH+CUR_NAME_WIDTH+NEW_NAME_WIDTH+DIF_WIDTH))

            print("".join(("Name".ljust(STAT_WIDTH),
                           new_equipment.name.ljust(NEW_NAME_WIDTH),
                           cur_equipment.name.ljust(CUR_NAME_WIDTH))))

            print("".join(("Power".ljust(STAT_WIDTH),
                           str(new_equipment.stats[0]).ljust(NEW_NAME_WIDTH),
                           str(cur_equipment.stats[0]).ljust(CUR_NAME_WIDTH),
                           str(new_equipment.stats[0] - cur_equipment.stats[0]).ljust(DIF_WIDTH))))

            print("".join(("Precision".ljust(STAT_WIDTH),
                           str(new_equipment.stats[1]).ljust(NEW_NAME_WIDTH),
                           str(cur_equipment.stats[1]).ljust(CUR_NAME_WIDTH),
                           str(new_equipment.stats[1] - cur_equipment.stats[1]).ljust(DIF_WIDTH))))

            print("".join(("Toughness".ljust(STAT_WIDTH),
                           str(new_equipment.stats[2]).ljust(NEW_NAME_WIDTH),
                           str(cur_equipment.stats[2]).ljust(CUR_NAME_WIDTH),
                           str(new_equipment.stats[2] - cur_equipment.stats[2]).ljust(DIF_WIDTH))))

            print("".join(("Vitality".ljust(STAT_WIDTH),
                           str(new_equipment.stats[3]).ljust(NEW_NAME_WIDTH),
                           str(cur_equipment.stats[3]).ljust(CUR_NAME_WIDTH),
                           str(new_equipment.stats[3] - cur_equipment.stats[3]).ljust(DIF_WIDTH))))
            
            print("-"*(STAT_WIDTH+CUR_NAME_WIDTH+NEW_NAME_WIDTH+DIF_WIDTH))

            choice = input("\nEquip " + new_equipment.name + "? (Y/N): ").lower()
            if choice == "y":
                unequipped_item = self.unequip(slot)
                self.actuallyEquip(new_equipment, slot)
                return unequipped_item
            elif choice == 'n':
                os.system("cls" if os.name == "nt" else "clear")
                return False

    def get(self, slot):
        return self.slots_dict.get(slot)
    
    def unequip(self, slot):
        return self.slots_dict.pop(slot)
    
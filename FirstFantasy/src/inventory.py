import items
import os

class Storage:
    def __init__(self, capacity):
        self.capacity = capacity
        self.item_list = []

    def add(self, item):
        # Is item stackable?
        if item.stack_limit > 1:
            # Determine if stackable item is already in item_list
            for i,x in enumerate(self.item_list):
                if x.name == item.name:
                    if x.stack_size < x.stack_limit:
                        self.item_list[i].stack_size += 1
                        return True
        
        # Is item_list full?
        if len(self.item_list) >= self.capacity:
            return False
        else:
            self.item_list.append(item)
            return True

    def remove(self, item_key):
        for i,x in enumerate(self.item_list):
            if x.name == item_key:
                if x.stack_size == 1:
                    self.item_list.pop(i)
                    return True
                else:
                    choice = input("Remove entire stack? (Y/N)").lower()
                    if choice == "y":
                        self.item_list.pop(i)
                    else:
                        self.item_list[i].stack_size -= 1
    
    # May be unnecessary to directly use an item like this
    def use(self, item_key):
        for i,x in enumerate(self.item_list):
            if x.name == item_key:
                return self.item_list[i].getOptions()
        return False
    
    def access(self, from_where):
        return
        
class Equipment():
    def __init__(self):
        self.slots_dict = {"Helm": None, 
                           "Coat": None, 
                           "Gloves": None,
                           "Leggings": None, 
                           "Boots": None,
                           "Right Hand": items.Sword("Rusty Sword", [0, 0, 0, 0]),
                           "Left Hand": None}
        
    def equip(self, new_equipment, accessed_from="zone"):
        slot = new_equipment.slot
        if self.slots_dict.get(slot) is not None:
            self.compareEquip(new_equipment, self.slots_dict.get(slot))
        else:
            self.actuallyEquip(new_equipment, slot)
        return True
    
    def actuallyEquip(self, new_equipment, slot):
        self.slots_dict[slot] = new_equipment
    
    def compareEquip(self, new_equipment, cur_equipment, slot):
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            STAT_WIDTH = 12
            CUR_NAME_WIDTH = len(cur_equipment.name) + 2
            NEW_NAME_WIDTH = len(new_equipment.name) + 2
            WIDTH = 4
            print ("".join(("Stat".ljust(STAT_WIDTH),
                           "New".ljust(NEW_NAME_WIDTH),
                           "Current".ljust(CUR_NAME_WIDTH),
                           "Difference".ljust(WIDTH))))

            print ("".join(("Name".ljust(STAT_WIDTH),
                           new_equipment.name.ljust(NEW_NAME_WIDTH),
                           cur_equipment.name.ljust(CUR_NAME_WIDTH))))

            print ("".join(("Power".ljust(STAT_WIDTH),
                           str(new_equipment.stats[0]).ljust(NEW_NAME_WIDTH),
                           str(cur_equipment.stats[0]).ljust(CUR_NAME_WIDTH),
                           str(new_equipment.stats[0] - cur_equipment.stats[0]).ljust(WIDTH))))

            print ("".join(("Precision".ljust(STAT_WIDTH),
                           str(new_equipment.stats[1]).ljust(NEW_NAME_WIDTH),
                           str(cur_equipment.stats[1]).ljust(CUR_NAME_WIDTH),
                           str(new_equipment.stats[1] - cur_equipment.stats[1]).ljust(WIDTH))))

            print ("".join(("Toughness".ljust(STAT_WIDTH),
                           str(new_equipment.stats[2]).ljust(NEW_NAME_WIDTH),
                           str(cur_equipment.stats[2]).ljust(CUR_NAME_WIDTH),
                           str(new_equipment.stats[2] - cur_equipment.stats[2]).ljust(WIDTH))))

            print ("".join(("Vitality".ljust(STAT_WIDTH),
                           str(new_equipment.stats[3]).ljust(NEW_NAME_WIDTH),
                           str(cur_equipment.stats[3]).ljust(CUR_NAME_WIDTH),
                           str(new_equipment.stats[3] - cur_equipment.stats[3]).ljust(WIDTH))))
            choice = input("\nEquip " + new_equipment.name + "? (Y/N)").lower()
            if choice == "y":
                self.actuallyEquip(new_equipment, slot)
                return True
            elif choice == 'n':
                os.system("cls" if os.name == "nt" else "clear")
                return False

    def unequip(self, item_key):
        return
    
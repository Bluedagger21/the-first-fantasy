import items

class Storage:
    def __init__(self, capacity):
        self.capacity = capacity
        self.inventory = []

    def add(self, item):
        # Is inventory full?
        if len(self.inventory) >= self.capacity:
            return False
        
        # Is item stackable?
        if item.stack_limit == 1:
            self.inventory.append(item)
            return True

        
    def remove(self, item_key):
    
    def use(self, item_key):
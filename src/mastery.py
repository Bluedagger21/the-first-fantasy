class Mastery:
    def __init__(self, type) -> None:
        self.type = type
        self.level = 1
        self.xp = 0

    def giveXP(self, xp):
        self.xp += xp
        self.checkLevel()
    
    def checkLevel(self):
        next_level_threshold = 1000 + (1000 * self.level * (.5 * self.level))
        if self.xp >= next_level_threshold:
            self.levelUp()
    
    def levelUp(self):
        self.level += 1
        print("Your mastery of the {} has leveled to {}!".format(self.type.__name__, self.level))
        self.checkLevel()

class MasteryList:
    def __init__(self, list = []) -> None:
        self.list = list

    def giveXP(self, item_type, xp_amount):
        self.getMastery(item_type).giveXP(xp_amount)

    def getMastery(self, item_type):
        for mastery in self.list:
            if mastery.type == item_type:
                return mastery
        
        # mastery type doesn't exist

        self.append(item_type)
        return self.getMastery(item_type)
    
    def append(self, item_type):
        self.list.append(Mastery(item_type))
    
    def getLevel(self, item_type):
        return self.getMastery(item_type).level
            
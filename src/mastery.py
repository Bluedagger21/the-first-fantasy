class Mastery():
    def __init__(self, type) -> None:
        self.type = type
        self.level = 1
        self.xp = 0

    def giveXP(self, xp):
        self.xp += xp
    
    def checkLevel(self):
        next_level_threshold = 1000 + (1000 * self.level * (.5 * self.level))
        if self.xp >= next_level_threshold:
            self.levelUp()
    
    def levelUp(self):
        self.level += 1
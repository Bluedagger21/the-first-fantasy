import random

class Status:
    def __init__(self, name, owner, target=None, duration=-1, phase=None) -> None:
        self.name = name
        self.duration = duration
        self.owner = owner
        self.target = target
        self.duration = duration
        self.phase = phase

    def tick(self, phase):
        if phase == self.phase:
            self.trigger()
            self.duration -= 1
            if self.duration == 0:
                print("The {} effect on {} expires.".format(self.name, self.owner))
                return False
            else:
                return True
        
    def trigger(self):
        pass

class Bleeding(Status):
    def __init__(self, name, owner, damage_per_turn) -> None:
        super().__init__(name, owner, duration=3, phase="BoT")
        self.damage_per_turn = damage_per_turn

    def trigger(self):
        self.owner.takeDamage(self.damage_per_turn, None)
        print("{} takes {} from bleeding.".format(self.owner.name, self.damage_per_turn))

class Poison(Status):
    def __init__(self, name, owner) -> None:
        super().__init__(name, owner, duration=-1, phase="BoT")
    
    def trigger(self):
        self.owner.takeDamage(self.owner.health * .1)
        print("{} takes {} damage from poison.".format(self.owner, self.damage_per_turn))
    
    def tick(self, phase):
        if phase == self.phase:
            if random.random() >= .5:
                print("The {} effect on {} expires.".format(self.name, self.owner))
                return False
            else:
                self.trigger()
                return True

class Shield(Status):
    def __init__(self, name, owner, target=None, duration=1, shield_amount=0) -> None:
        super().__init__(name, owner, target, duration)
        self.shield_amount = shield_amount

class StatusList():
    def __init__(self, list=None, owner=None) -> None:
        self.owner = owner
        if list is None:
            self.status_list = []
        else:
            self.status_list = list
    
    def append(self, status):
        if isinstance(status, str):
            self.status_list.append(Status(status, self.owner))
        else:
            self.status_list.append(status)
            return True
    
    def remove(self, name):
        if isinstance(name, str):
            for status in self.status_list:
                if status.name == name:
                    self.status_list.remove(status)
                    return True
            return False
        if isinstance(name, Status):
            self.status_list.remove(status)
            return True

    def exists(self, name):
        if isinstance(name, str):
            for status in self.status_list:
                if status.name == name:
                    return True
            return False
        if isinstance(name, Status):
            if name in self.status_list:
                return True
            else:
                return False
    
    def tick(self, phase):
        for status in self.status_list:
            status.tick(phase)
            if status.duration == 0:
                self.remove(status)

    def clear(self):
        for status in self.status_list:
            if (status.duration >= 0) and (status.phase == None):
                self.status_list.remove(status)

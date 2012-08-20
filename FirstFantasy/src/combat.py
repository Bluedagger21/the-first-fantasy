'''
Last changed by: Dale Everett
'''
import os
import loottable
import time

def getAction(a,b):
    """Display combat information and prompt for action"""
    os.system("CLS")
    print b.name
    print "Health: " + repr(b.health) + "/" + repr(b.getMaxHealth())
    print "P: {:2} P: {:2} T: {:2} V: {:2}".format(b.stat_list[0],b.stat_list[1],b.stat_list[2],b.stat_list[3])
    print "----------------------VERSUS"
    print a.name
    print "Health: " + repr(a.health) + "/" + repr(a.getMaxHealth())
    print "P: {:2} P: {:2} T: {:2} V: {:2}".format(a.stat_list[0]+a.equipment_stat_list[0],a.stat_list[1]+a.equipment_stat_list[1],a.stat_list[2]+a.equipment_stat_list[2],a.stat_list[3]+a.equipment_stat_list[3])
    print "\n[ACTIONS]-------------------"
    choice = raw_input("(A)ttack    (I)nventory    (E)nemy Info: ").lower()
    if choice == "a" or choice == "i" or choice == "e":
        return choice
    else:
        return

def combat(a,b):
    """State machine that controls combat flow between a (typically the player) b (typically player's enemy)"""
    a_status = a.status
    b_status = b.status
    c_state = None
    n_state = "standby"
    while True:
        c_state = n_state
        
        if c_state == "standby":
            action = getAction(a,b)
            if action == "a":
                n_state = "attack"
            elif action == "i":
                n_state = "inventory"
            elif action == "e":
                n_state = "info"
            else:
                n_state = n_state
                
        elif c_state == "effects":
            pass
        
        elif c_state == "attack":
            a_status = a.status
            if a_status == "normal":
                a.attack(b)
                time.sleep(1)
            b_status = b.status
            if b_status == "normal":
                b.attack(a)
                time.sleep(1)
            a_status = a.status
            n_state = "endturn"
            
        elif c_state == "endturn":
            if a_status == "dead":
                print a.name + " has been defeated!"
                os.system("PAUSE")
                break
            elif b_status == "dead":
                print b.name + " has been defeated!"
                n_state = "win"
            else:
                n_state = "standby"
                
        elif c_state == "win":
            loot = loottable.Loot(b.level)
            if loot[1] != None:
                a.giveItem(loot[1])
            a.giveGold(loot[0])
            a.giveExp((a.exp_needed/(9 + a.level))*(b.level/a.level))
            os.system("PAUSE")
            break
        
        elif c_state == "inventory":
            a.getInventory()
            n_state = "standby"
            
        elif c_state == "info":
            b.getCharacterSheet()
            os.system("PAUSE")
            n_state = "standby"

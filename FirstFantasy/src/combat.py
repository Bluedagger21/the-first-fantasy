'''
Last changed by: Dale Everett
'''
import os
import loottable
import time
import random


def getAction(a, b):
    """Display combat information and prompt for action"""
    os.system("cls" if os.name == "nt" else "clear")
    print b.name
    print "Health: " + repr(b.health) + "/" + repr(b.getMaxHealth())
    print "P: {:2} P: {:2} T: {:2} V: {:2}".format(
           b.stat_list[0], b.stat_list[1], b.stat_list[2], b.stat_list[3])
    print "----------------------VERSUS"
    print a.name
    print "Health: " + repr(a.health) + "/" + repr(a.getMaxHealth())
    print "P: {:2} P: {:2} T: {:2} V: {:2}".format(
           a.stat_list[0] + a.equipment_stat_list[0], a.stat_list[1] +
           a.equipment_stat_list[1], a.stat_list[2] + a.equipment_stat_list[2],
           a.stat_list[3] + a.equipment_stat_list[3])
    print "\n[ACTIONS]-------------------"
    choice = raw_input("(A)ttack    (I)nventory\n(E)nemy Info    (R)un Away: ").lower()
    if choice == "a" or choice == "i" or choice == "e" or choice == "r":
        return choice
    else:
        return


def combat(a, b):
    """
    State machine that controls combat flow between a (typically the player)
    and b (typically player's enemy)
    """
    c_state = None
    n_state = "standby"
    while True:
        c_state = n_state

        if c_state == "standby":
            action = getAction(a, b)
            if action == "a":
                n_state = "a_attack"
            elif action == "i":
                n_state = "inventory"
            elif action == "e":
                n_state = "info"
            elif action == "r":
                n_state = "run"
            else:
                n_state = n_state
            print "----------------------------"  # Newline

        elif c_state == "effects":
            pass

        elif c_state == "a_attack":
            if "skip" in a.status:
                print a.name + " skipped their turn."
                a.status.remove("skip")
            elif "normal" in a.status:
                a.attack(b)
            time.sleep(1)
            if "dead" in b.status:
                n_state = "endturn"
            else:
                n_state = "b_attack"
        elif c_state == "b_attack":
            if "skip" in b.status:
                print b.name + " skipped their turn."
                b.status.remove("skip")
                time.sleep(1)
            elif "caught" in b.status:
                time.sleep(1)
                b.attack(a)
                b.status.remove("caught")
                raw_input("Press \"Enter\" to continue...")
            elif "normal" in a.status:
                b.attack(a)
                time.sleep(1)
            n_state = "endturn"

        elif c_state == "endturn":
            if "dead" in a.status:
                print a.name + " has been defeated!"
                raw_input("Press \"Enter\" to continue...")
                break
            elif "dead" in b.status:
                print b.name + " has been defeated!"
                n_state = "win"
            else:
                n_state = "standby"

        elif c_state == "win":
            loot = loottable.Loot(b.level)
            if loot[1] is not None:
                a.giveItem(loot[1])
            a.giveGold(loot[0])
            a.giveExp((a.exp_needed / (9 + a.level)) * (b.level / a.level))
            raw_input("Press \"Enter\" to continue...")
            break

        elif c_state == "inventory":
            a.getInventory("combat")
            n_state = "standby"

        elif c_state == "info":
            b.getCharacterSheet()
            raw_input("Press \"Enter\" to continue...")
            n_state = "standby"
        
        elif c_state == "run":
            if random.randrange(1,3) == 1:
                print "You were able to get away!"
                raw_input("Press \"Enter\" to continue...")
                break
            else:
                print "You couldn't get away and %s caught you!" % b.name
                n_state = "b_attack"
                b.status.append("caught")

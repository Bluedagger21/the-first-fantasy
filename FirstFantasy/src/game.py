'''
Last changed by: Dale Everett
'''
import characters
import world
import combat
import cPickle
import sys
import os

player = None
worldmap = None


def titlescreen():
    """Display title and prompt whether to start a new game, continue, or quit"""
    choice = ''
    while True:
        os.system("CLS")
        print "The First Fantasy"
        print "Copyright (C) 2012  Dale Everett\n\n"
        while True:
            print "(N)ew Game    (C)ontinue    (Q)uit"
            choice = raw_input().lower()
            if choice == 'n' or choice == 'c' or choice == 'q':
                break
        if choice == 'n':
            newgame()
            break
        elif choice == 'c':
            tmp_bool = continuegame() 
            if tmp_bool == True:
                break  
        elif choice == 'q':
            sys.exit()
            break

def newgame():
    """Get player name and create new world"""
    global worldmap
    global player
    print "\n"
    player = characters.Player(raw_input("Enter your name: "))
    worldmap = world.Map()
    print "Prepare to begin your journey..."
    os.system("PAUSE")
    
def continuegame():
    """Prompt to choose saved game and load player and worldmap states"""
    global worldmap
    global player
    print "Retrieving current directory..."
    home_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
    print home_dir
    while True:
        os.system("CLS")
        if not os.path.exists(home_dir+"\saves"):
            print "Creating saves directory..."
            os.makedirs(home_dir+'\saves')
        for files in os.listdir(home_dir+"\saves"):
            if files.endswith(".bin"):
                print files[:-4]
        saved_file = raw_input("\nType filename to load (C to cancel): ")
        if os.path.exists(home_dir+"\saves\\"+saved_file+".bin"):
            print "Loading game..."
            f = open(home_dir+'\saves\\'+saved_file+'.bin', 'rb')
            player = cPickle.load(f)
            worldmap = cPickle.load(f)
            f.close()
            print "...Done!"
            os.system("PAUSE")
            return True
        elif saved_file == 'c' or saved_file == 'C':
            return False
        else:
            continue

def homescreen():
    """Displays current location information and prompts for actions
    
    NOTE -- Need to reduce this function into something more manageable"""
    choice = ''
    while True:
        current_zone = worldmap.loadZone()
        os.system("CLS")
        choice = current_zone.getOptions()
        if choice == 'e':
            os.system("CLS")
            explore(current_zone)
        elif choice == 'c':
            os.system("CLS")
            player.getCharacterSheet()
            os.system("PAUSE")
        elif choice == 'r':
            cost = player.level * 10 + 15
            print "Cost: {}g".format(cost)
            if raw_input("Accept? (Y/N): ").lower() == 'y':
                if player.gold >= cost:
                    player.gold -= cost
                    player.health = player.getMaxHealth()
                    print player.name + " has returned to full health!"
                else:
                    print "You don't have enough gold!"
                os.system("PAUSE")
        elif choice == 'i':
            os.system("CLS")
            player.getInventory()               
        elif choice == 't':
            os.system("CLS")
            worldmap.printMap()
            print "You make your way to " + worldmap.current_zone.z_name
            if worldmap.current_zone.z_type == "wild":
                explore(worldmap.current_zone)
            else:
                os.system("PAUSE")
        elif choice == 'q':
            sys.exit()
        elif choice == 's':
            os.system("CLS")
            home_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
            if not os.path.exists(home_dir+'\saves'):
                os.makedirs(home_dir+'\saves')
            print home_dir
            f = open(home_dir+'\saves\\'+player.name+'.bin', 'wb')
            print "Saving game..."
            
            cPickle.dump(player, f, protocol=0)
            cPickle.dump(worldmap, f, protocol=0)
            f.close()
            print "...Done!"
            os.system("PAUSE")
        else:
            continue
                       
def explore(current_zone):
    """Decides if an encounter occurs or not"""
    os.system("CLS")
    action = current_zone.getAction()
    if action == "encounter":
        opponent = current_zone.getEnemy()
        combat.combat(player, opponent)
    elif action == "nothing":
        print "Nothing of interest was found..."
        os.system("PAUSE")
    
        
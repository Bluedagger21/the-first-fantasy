#! /usr/bin/python3.9
import game

if __name__ == '__main__':

    done = False
    game.titlescreen()

    while done is False:
        # Run loop
        done = game.homescreen()

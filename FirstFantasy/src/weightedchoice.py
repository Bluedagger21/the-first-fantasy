'''
Last changed by: Dale Everett
'''
import random


def weighted_choice_sub(weights):
    """ Returns weighted random index of given weights """
    rnd = random.random() * sum(weights)
    for i, w in enumerate(weights):
        rnd -= w
        if rnd < 0:
            return i

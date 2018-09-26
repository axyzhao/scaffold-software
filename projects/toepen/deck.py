#! /usr/bin/env python

CARDWIDTH = 100
CARDHEIGHT = 100
MARGIN = 10

class Deck:
    def __init__(self):
        self.suits = ['spades', 'hearts', 'diamonds', 'clubs']
        self.values = ['7', '8', '9', '10', 'J', 'Q' 'K' 'A']

#!/usr/bin/env python

import sys
import random

class Game:

    def __init__(self):
        self.players = []
        self.playMode = False
        self.deck = Deck()
        self.numPlayers = 8
        self.toep = 0

    def isMultiplayer(self):
        return self.playMode

    def setPlayers(self, number):
        self.numPlayers = int(number)
        if self.numPlayers > 8:
            self.numPlayers = 8
            print("Maximum number of players exceeded! The number of players has been set to 8")

        for i in range(self.numPlayers):
            p = self.players.append(Player(i, False))

    def setCPUs(self, number):
        self.numCPUs = int(number)
        if self.numPlayers == 1 and self.numCPUs == 0:
            self.numCPUs = 2
            print("You can't play by yourself! We've made you two computer friends to play with you.")

        if (self.numCPUs + self.numPlayers) > 8:
            self.numCPUs = 8 - self.numPlayers
            print("Maximum number of players exceeded! The number of CPUs has been set to: ", self.numCPUs)

        for i in range(self.numCPUs):
            self.players.append(Player(i, True))

        for p in self.players:
            p.setGame(self)

    def displayRules(self):
        print("rules")

    def startGame(self):
        startChoice = input("OPENING GAME SCREEN\n\n\n\n start (S), rules (R), quit (Q): ")
        if (startChoice == 's' or startChoice == 'S'):
    #start choice means what they pick at the beginning screen
            mode = input("Multiplayer/single player? (y/n): ")
            if (mode == 'y' or mode == 'Y'):
                self.playMode = True

            if self.playMode:
                print("You have selected multiplayer mode.\n")

            else:
                print("You have selected single player mode. \n")

            if self.isMultiplayer():
                numPlayers = input("How many people are playing? (Maximum is 8) \n")

                isInt = True

                try:
                   val = int(numPlayers)
                except ValueError:
                   print("Input must be a positive integer!")
                   isInt = False

                if isInt:
                    self.setPlayers(numPlayers)
            else:
                self.setPlayers(1)

            if self.numPlayers <= 8:
                numCPUs = input("Okay, great. How many CPUs would you like? Maximum total players is 8, including you. \n")

                isInt = True
                try:
                   val = int(numCPUs)
                except ValueError:
                   print("Input must be a positive integer!")
                   isInt = False

                if isInt:
                    self.setCPUs(numCPUs)

            go = input("Fantastic! Let's get started. Press any key to continue.\n")

            if go:
                self.play()

#rules option
        elif (startChoice == 'r' or startChoice == 'R'):
            self.displayRules()

    #quitting the game
        elif (startChoice == 'q' or startChoice == 'Q'):
            quit()

    def increaseToep(self):
        self.toep = self.toep + 1

    def play(self):
        print("play!")
        self.deck.shuffle()
        for p in self.players:
            p.cards = self.deck.deal()

        self.takeTurn()

        print("")

    def takeTurn(self):
        #check if anyone has 0 lives
        #go around each player -- if real player, display options. If not, do AI stuff
        #display previous players

        for p in self.players:
            print("It's your turn!")

            #what would you like to do? fold, toep, checkscore, play which cards?
            action = input("What do you want to do?\nFold (F), toep (T), check game stats (C), play a card (P)\n")

            if action == 't' or action == 'T':
                p.toep()

        print("Round over. Putting discarded cards back into deck...\n")
        self.deck.reshuffle()


class Deck:
    def __init__(self):
        self.suits = ['spades', 'hearts', 'diamonds', 'clubs']
        self.values = ['7', '8', '9', '10', 'J', 'Q' 'K' 'A']
        self.cards = [Card(value, color) for value in self.suits for color in self.suits]

    def shuffle(self):
        print("Shuffling deck...\n")
        # Start from the last element and swap one by one. We don't
        # need to run for the first element that's why i > 0
        for i in range(len(self.cards) - 1, 0, -1):
            # Pick a random index from 0 to i
            j = random.randint(0,i)

            # Swap arr[i] with the element at random index

            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def reshuffle(self):
        self.cards = [Card(value, color) for value in self.suits for color in self.suits]
        self.shuffle()

    def deal(self):
        res = []

        for i in range(len(self.cards) - 1, 0, -1):
            # Pick a random index from 0 to i
            j = random.randint(0,i)
            res.append(self.cards[i])
            del self.cards[i]

        return res

class Player:
    def __init__(self, name, isCPU):
        self.name = str(name)
        self.isCPU = isCPU
        self.lives = 10

    def setGame(self, game):
        self.game = game

    def setCards(self, cards):
        self.cards = cards

    def checkLives(self):
        print("You have " + self.lives + " lives left.")

    #def mulligan(self):
    def toep(self):
        self.game.increaseToep()

    def lost(self):
        return (self.lives == 0)

    #def fold(self):
    #def play card
    #def discard

class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

def main():
    game = Game()
    game.startGame()

if __name__ == "__main__":
    main()

def quit():
    print("you have left the game")


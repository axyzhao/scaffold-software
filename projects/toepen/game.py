#!/usr/bin/env python

import sys
import random

class Game:

    def __init__(self):
        self.players = []
        self.currentStack = []
        self.playMode = False
        self.deck = Deck()
        self.numPlayers = 8
        self.toep = 1
        self.suit = ""

    def isMultiplayer(self):
        return self.playMode

    def setPlayers(self, number):
        self.numPlayers = int(number)
        if self.numPlayers > 8:
            self.numPlayers = 8
            print("Maximum number of players exceeded! The number of players has been set to 8")

        for i in range(self.numPlayers):
            p = self.players.append(Player("Player " + str(i)))
        for p in self.players:
            p.setGame(self)

    # def setCPUs(self, number):
    #     self.numCPUs = int(number)
    #     if self.numPlayers == 1 and self.numCPUs == 0:
    #         self.numCPUs = 2
    #         print("You can't play by yourself! We've made you two computer friends to play with you.")
    #
    #     if (self.numCPUs + self.numPlayers) > 8:
    #         self.numCPUs = 8 - self.numPlayers
    #         print("Maximum number of players exceeded! The number of CPUs has been set to: ", self.numCPUs)
    #
    #     for i in range(self.numCPUs):
    #         self.players.append(Player("CPU " + str(i), True))
    #
    #     for p in self.players:
    #         p.setGame(self)

    def displayRules(self):
        print("rules")

    def startGame(self):
        startChoice = input("OPENING GAME SCREEN\n\n\n\n start (S), rules (R), quit (Q): ")
        if (startChoice == 's' or startChoice == 'S'):
    #start choice means what they pick at the beginning screen
            # mode = input("Multiplayer/single player? (M/S): ")
            # if (mode == 'm' or mode == 'M'):
            #     self.playMode = True
            #
            # if self.playMode:
            #     print("You have selected multiplayer mode.\n")
            #
            # else:
            #     print("You have selected single player mode. \n")

            # if self.isMultiplayer():
            numPlayers = input("How many people are playing? (Maximum is 8) \n")

            isInt = True

            try:
               val = int(numPlayers)
            except ValueError:
               print("Input must be a positive integer!")
               isInt = False

            if isInt:
                self.setPlayers(numPlayers)
            # else:
            #     self.setPlayers(1)
            #
            # if self.numPlayers <= 8:
            #     numCPUs = input("Okay, great. How many CPUs would you like? Maximum total players is 8, including you. \n")
            #
            #     isInt = True
            #     try:
            #        val = int(numCPUs)
            #     except ValueError:
            #        print("Input must be a positive integer!")
            #        isInt = False
            #
            #     if isInt:
            #         self.setCPUs(numCPUs)
            #
            go = input("Fantastic! Let's get started. Press any key to continue.\n")

            if go:
                print("*********************************************************************************************************")
                self.play()

#rules option
        elif (startChoice == 'r' or startChoice == 'R'):
            self.displayRules()

    #quitting the game
        elif (startChoice == 'q' or startChoice == 'Q'):
            self.quit()

    def quit(self):
        print("you have left the game :(")

    def increaseToep(self):
        self.toep = self.toep + 1

    def play(self):
        self.deck.shuffle()
        print("Dealing cards...\n")

        for p in self.players:
            p.setCards(self.deck.deal())

        self.playRound(0)

        print("")

    def playTrick(self):
        startingPlayer = self.playRound(0)
        while startingPlayer >= 0:
            self.playRound(startingPlayer)

    def playRound(self, startingPlayer):
        for i in range(startingPlayer, startingPlayer + len(self.players)):
            p = self.players[i % len(self.players)]

            if (p.inGame):
                self.takeTurn(self.players[i % len(self.players)])

        maxVal = -1 * pow(10, 10)
        maxName = 0
        for tup in self.currentStack:
            tupVal = tup[1].value
            ranking = self.deck.values.index(tupVal)
            if maxVal != max(maxVal, ranking):
                maxVal = ranking
                maxName = tup[0]

        print("The winner is..." + maxName + "! They get to start the next round off.")
        print("Round over. Putting discarded cards back into deck...\n")
        self.deck.reshuffle()

        #TODO: need to return max player
        # Everyone else has lost " + str(self.toep) + " lives.")

        for p in self.players:
            if p.inGame:
                p.lives = p.lives - self.toep
            if p.lives <= 0:
                print(p.name + " has lost! The game is over.")
                return -1

    def takeTurn(self, player):
        #check if anyone has 0 lives
        #go around each player -- if real player, display options. If not, do AI stuff
        #display previous players

        print("*********************************************************************************************************")
        print("Hey, " + player.name + "! It's your turn!\n")
        player.displayCards()

        #what would you like to do? fold, toep, checkscore, play which cards?
        action = input("What do you want to do?\nMulligan (M), fold (F), toep (T), check game stats (C), play a card (P)\n")
        action = action.lower()

        mulliganFlag = False
        toepFlag = False

        while(True):
            if action == 'm' or action == 'M':
                if mulliganFlag == False:
                    mulliganFlag = True
                    print("\n")
                    player.mulligan()
                    print("\n")
                else:
                    print("You have already mulligan'd this round.")

                action = input("What do you want to do?\nFold (F), toep (T), check game stats (C), play a card (P)\n")
                action = action.lower()

            elif action == 't' or action == 'T':
                if toepFlag == False:
                    toepFlag = True
                    print("\n")
                    player.toep()
                    print("\n")
                else:
                    print("You have already toeped this round.\n")
                action = input("What do you want to do?\nMulligan (M), fold (F), check game stats (C), play a card (P)\n")
                action = action.lower()
            elif action == 'c' or action == 'C':
                print("\n")
                player.checkGameStats()
                print("\n")
                action = input("What do you want to do?\nMulligan (M), fold (F), toep (T), check game stats (C), play a card (P)\n")
                action = action.lower()
            elif action == 'f' or action == 'F':
                print("\n")
                player.fold()
                return
                print("\n")
            elif action == 'p' or action == 'P':
                print("\n")
                player.playCard(self.suit)
                return
            else:
                print("You selected an invalid option.\n")
                action = input("What do you want to do?\nMulligan (M), fold (F), toep (T), check game stats (C), play a card (P)\n")
                action = action.lower()

class Deck:
    def __init__(self):
        self.suits = ['spades', 'hearts', 'diamonds', 'clubs']
        self.values = ['7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(value, color) for value in self.values for color in self.suits]

    def shuffle(self):
        print("Shuffling deck...\n")
        # Start from the last element and swap one by one. We don't
        # need to run for the first element that's why i > 0
        for i in range(len(self.cards) - 1, 0, -1):
            # Pick a random index from 0 to i
            j = random.randint(0,i)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def reshuffle(self):
        self.cards = [Card(value, color) for value in self.values for color in self.suits]
        self.shuffle()

    def deal(self):
        res = []

        counter = 0

        for i in range(len(self.cards) - 1, 0, -1):
            # Pick a random index from 0 to i
            if counter == 4:
                break

            j = random.randint(0,i)
            res.append(self.cards[j])
            del self.cards[j]
            counter = counter + 1
        return res

class Player:
    def __init__(self, name):
        self.name = str(name)
        # self.isCPU = isCPU
        self.lives = 10
        self.inGame = True

    def setGame(self, game):
        self.game = game

    def setCards(self, cards):
        self.cards = cards

    def checkGameStats(self):
        print("********************************GAME INFO******************************")
        print("Your lives: " + str(self.lives))

        for p in self.game.players:
            if p.name != self.name:
                print(p.name + "'s lives: " + str(p.lives))

        self.displayCards()
        print("The cards played thus far in the round are: ")

        for c in self.game.currentStack:
            print("(" + str(c[1].value) + ", " + str(c[1].color) + ")", end=" ")
            print("\n")

        print("Current toep: " + str(self.game.toep))
        print("Current suit: " + str(self.game.suit))

    def mulligan(self):
        print("mulligan!")

    def toep(self):
        self.game.increaseToep()

    def displayCards(self):
        print("Your cards: ")
        for c in self.cards:
            print("(" + str(c.value) + ", " + str(c.color) + ")", end=" ")
            print("\n")

    def lost(self):
        return (self.lives == 0)

    def fold(self):
        self.lives = self.lives - self.game.toep
        print("You have folded and exited the game. You have also lost " + str(self.game.toep) + " lives and now have " + str(self.lives) + " left.")
        self.inGame = False

    def playCard(self, suit):
        self.displayCards()
        choice = input("Which card would you like to play? If you have the suit " + suit + ", you must play a card of that suit. Otherwise, you can play a different card.\nDenote the card you would like to play by typing J, hearts. Ex: Q, spades\n")

        raw_card = [x.strip() for x in choice.split(',')]

        while len(raw_card) < 2:
            print("This is not a valid card! Please specify a card in your hand.")
            choice = input("Which card would you like to play? If you have the suit " + suit + ", you must play a card of that suit. Otherwise, you can play a different card.\nDenote the card you would like to play by typing J, hearts. Ex: Q, spades\n")
            raw_card = [x.strip() for x in choice.split(',')]

        hasCard = False

        while(hasCard != True):
            for c in self.cards:
                if (c.value == raw_card[0] and c.color == raw_card[1]):
                    hasCard = True
                    card = c

            if hasCard == False:
                print("This card is not in your hand! Please specify a card in your hand.")
                choice = input("Which card would you like to play? If you have the suit " + suit + ", you must play a card of that suit. Otherwise, you can play a different card.\nDenote the card you would like to play by typing J, hearts. Ex: Q, spades\n")
                raw_card = [x.strip() for x in choice.split(',')]

        hasSuit = True

        while(hasSuit == True and suit != card.color):
            hasSuit = False

            for c in self.cards:
                if c.color == suit:
                    hasSuit = True

            if hasSuit and card.color != suit and len(suit) > 0:
                print("The card chosen is not of the required suit! If you have the current round's suit, you must play that card.")
                choice = input("Which card would you like to play? If you have the suit " + suit + ", you must play a card of that suit. Otherwise, you can play a different card.\nDenote the card you would like to play by typing J, hearts. Ex: Q, spades\n")

                raw_card = [x.strip() for x in choice.split(',')]

                hasCard = False

                while(hasCard != True):
                    for c in self.cards:
                        if c.value == raw_card[0] and c.color == raw_card[1]:
                            hasCard = True
                            card = c

                    if hasCard == False:
                        print("This card is not in your hand! Please specify a card in your hand.")
                        choice = input("Which card would you like to play? If you have the suit " + suit + ", you must play a card of that suit. Otherwise, you can play a different card.\nDenote the card you would like to play by typing J, hearts. Ex: Q, spades")
                        raw_card = [x.strip() for x in choice.split(',')]

        self.cards.remove(card)
        print("You have removed " + str(card.value) + ", " + str(card.color) + " from your deck.")
        self.game.currentStack.append((self.name, card))

#TODO: only one that sets game suit is the first player
        self.game.suit = raw_card[1]

class Card:
    def __init__(self, value, color):
        self.value = value
        self.color = color

    def returnCard(self):
        return (self.value, self.color)

def main():
    game = Game()
    game.startGame()

if __name__ == "__main__":
    main()



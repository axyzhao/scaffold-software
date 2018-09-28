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
        elif self.numPlayers < 2:
            self.numPlayers = 2
            print("You can't play this game by yourself! The number of players has been set to 2")

        for i in range(self.numPlayers):
            p = self.players.append(Player("Player " + str(i)))
        for p in self.players:
            p.setGame(self)
        self.leadPlayer = self.players[0]

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
        print("Players and cards\n"
        "Toepen is a fast trick-taking game for three to eight players. It is played with a 32-card pack, with the cards in each suit ranking 10 (highest), 9, 8, 7, A, K, Q, J (lowest).\n"
        "The basic object of each hand is to win the last trick.\n\n"
        "Deal\n"
        "The cards are dealt clockwise so that each player receives four cards.\n After the deal, the undealt portion of the pack is left face-down in the middle of the table.\n"
        "Then any player whose hand consists entirely of As, Ks, Qs, and Js may discard her hand face downward and deal herself a new one (called a mulligan).\n"
        "Indeed, any player may discard her hand face downward and deal herself a new one, but there is a risk. \n"
        "When a hand has been discarded in this way, it may be challenged by any other player, by turning it face upwards:\n"
        "if it is found to contain a 10,9,8 or 7 the discarder loses one life (but keeps her new hand) while if it really consists \n"
        "entirely of As,Ks,Qs and Js the challenger loses one life.\n\n"

        "Play of the cards\n"
        "The player on dealer's left leads to the first trick. Players must follow suit if possible, otherwise they may play any card.\n"
        "A trick is won by the highest card of the suit led. The winner of a trick leads to the next trick.\n\n"

        "Knocking\n"
        "At any time during a hand, once all the players have had an opportunity to pick up their cards, a player may increase the penalty by calling a toep. \n"
        "This increases the value of the hand by one life. When a player knocks, the other players may stay in, risking losing this extra life; or may fold, losing \n"
        "the current stake and taking no further part in the hand.\n"

        "The last player to knock may not knock again on the same hand, until someone else has knocked.\n"

        "Those who stay in to the end of the hand lose one more life than the total number of knocks. So for example if there are no knocks, everyone except\n"
        "the winner of the last trick loses one life; if there was one knock everyone who stayed in, except for the winner of the last trick, loses two lives, and so on.\n"

        "Those who fold on the first knock immediately lose one life; those who fold on the second knock lose two lives and so on - that is, by folding you\n"
        "lose the same amount you would have lost if the game had gone to the end with no further knocks and you lost the last trick.\n"

        "If a player knocks and everyone else folds, the player left in wins that hand (losing no life) and deals the next.\n"

        "If the winner of a trick folds after playing the winning card to the trick, but before the following trick has begun, the turn to lead to\n"
        "the next trick passes to the next player to the left who has not yet folded.\n"

        "A player may not knock and fold on her own knock.\n")

    def startGame(self):
        startChoice = input("OPENING GAME SCREEN\n\n\n\n start (S), rules (R), quit (Q): ")

        while True:
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
                while(True):
                    isInt = True
                    numPlayers = input("How many people are playing? (Maximum is 8) \n")
                    try:
                       val = int(numPlayers)
                    except ValueError:
                       isInt = False
                       print("Input must be a positive integer!")

                    if isInt:
                        self.setPlayers(numPlayers)
                        break
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
                break

    #rules option
            elif (startChoice == 'r' or startChoice == 'R'):
                self.displayRules()
                startChoice = input("OPENING GAME SCREEN\n\n\n\n start (S), rules (R), quit (Q): ")

        #quitting the game
            elif (startChoice == 'q' or startChoice == 'Q'):
                self.quit()
                break

    def quit(self):
        print("you have left the game :(")

    def increaseToep(self):
        self.toep = self.toep + 1

    def play(self):
        self.deck.shuffle()
        print("Dealing cards...\n")

        for p in self.players:
            p.setCards(self.deck.deal())

        self.playTrick()

        print("")

    def playTrick(self):
        startingPlayer = self.playRound(0)

        while startingPlayer >= 0:
            startingPlayer = self.playRound(startingPlayer)
            self.leadPlayer = self.players[startingPlayer]

        if startingPlayer == -1:
            return
        elif startingPlayer == -2:
            return


    def playRound(self, startingPlayer):
        counter = 0
        for i in range(startingPlayer, startingPlayer + len(self.players)):
            p = self.players[i % len(self.players)]

            if (p.inGame):
                res = self.takeTurn(self.players[i % len(self.players)])
                if res == -1:
                    winner = p
                    print("Round over. The winner is " + winner.name)
                    return -2

        maxVal = -1 * pow(10, 10)
        #store max card value from cards in the current pile

        maxName = ""
        for tup in self.currentStack:
            #card value
            tupVal = tup[1].value

            ranking = self.deck.values.index(tupVal)

            if maxVal != max(maxVal, ranking) and tup[1].color == self.suit:
                maxVal = ranking
                maxName = tup[0]

        print("The winner of the trick is " + maxName + "! They get to start the next trick off.")
        print("Putting discarded cards back into deck...\n")
        self.deck.reshuffle()

        raw_name = maxName.split(' ')

        leadPlayer = self.players[int(raw_name[1])]
        self.leadPlayer = leadPlayer

        #TODO: need to return max player
        # Everyone else has lost " + str(self.toep) + " lives.")

        for p in self.players:
            if p.inGame:
                p.lives = p.lives - self.toep
            if p.lives <= 0:
                print(p.name + " has lost! The game is over.")

                maxLives = -1000
                for p in self.players:
                    if maxLives != max(maxLives, p.lives):
                        maxLives = p.lives
                        champ = p

                print(champ.name + " is the ultimate winner, with " + str(champ.lives) + " lives.")

                return -1

        return int(raw_name[1])

    def takeTurn(self, player):
        #check if anyone has 0 lives
        #go around each player -- if real player, display options. If not, do AI stuff
        #display previous players

        print("*********************************************************************************************************")
        print("Hey, " + player.name + "! It's your turn!\n")
        player.displayCards()

        #what would you like to do? fold, toep, checkscore, play which cards?
        action = input("What do you want to do?\nMulligan (M), fold (F), toep (T), check game stats (C), play a card (P), review rules (R)\n")
        action = action.lower()

        mulliganFlag = False
        toepFlag = False

        while(True):
            if action == 'm':
                if mulliganFlag == False:
                    mulliganFlag = True
                    print("\n")
                    player.mulligan()
                    print("\n")
                else:
                    print("You have already mulligan'd this round.")

                action = input("What do you want to do?\nFold (F), toep (T), check game stats (C), play a card (P), review rules (R)\n")
                action = action.lower()

            elif action == 't':
                if toepFlag == False:
                    toepFlag = True
                    print("\n")
                    player.toep()
                    print("\n")
                else:
                    print("You have already toeped this round.\n")
                action = input("What do you want to do?\nMulligan (M), fold (F), check game stats (C), play a card (P), review rules (R)\n")
                action = action.lower()
            elif action == 'c':
                print("\n")
                player.checkGameStats()
                print("\n")
                action = input("What do you want to do?\nMulligan (M), fold (F), toep (T), check game stats (C), play a card (P), review rules (R)\n")
                action = action.lower()
            elif action == 'f':
                print("\n")
                player.fold()
                return
                print("\n")
            elif action == 'p':
                print("\n")
                return player.playCard(self.suit)
            elif action == 'r':
                print("\n")
                player.reviewRules()
                action = input("What do you want to do?\nMulligan (M), fold (F), toep (T), check game stats (C), play a card (P), review rules (R)\n")
                action == action.ower()
            else:
                print("You selected an invalid option.\n")
                action = input("What do you want to do?\nMulligan (M), fold (F), toep (T), check game stats (C), play a card (P), review rules (R)\n")
                action = action.lower()

class Deck:
    def __init__(self):
        self.suits = ['spades', 'hearts', 'diamonds', 'clubs']
        self.values = ['J', 'Q', 'K', 'A', '7', '8', '9', '10']
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

    def reviewRules(self):
        self.game.displayRules()

    def mulligan(self):
        isValid = True

        for c in self.cards:
            if c.value == '7' or c.value == '8' or c.value == '9' or c.value == '10':
                isValid = False
            self.game.deck.cards.append(c)

        print("You have swapped your four cards for four new ones.")
        self.setCards(self.game.deck.deal())
        self.displayCards()

        for p in self.game.players:
            if p.name != self.name:
                print("A challenger approaches...\n")
                print("Hello, " + p.name)
                callout = input(self.name + " has chosen to mulligan. Do you challenge their choice? (y/n)\n")
                callout.lower()
                if callout == 'y':
                    caller = p
                    break

        if callout == 'y':
            if isValid == True:
                print(caller.name + " has challenged " + self.name + "'s mulligan, and is wrong. Thus they lose a life.\n")
                caller.lives = caller.lives - 1
                print("Back to " + self.name + " !")
            else:
                print(caller.name + " has challenged " + self.name + "'s mulligan, and is correct. Thus " + self.name + " loses a life.\n")
                self.lives = self.lives -1
                print("Back to " + self.name + " !")
        else:
            print("No challenges. Phew\n")
            print("Back to " + self.name + " !")

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

            if self.game.leadPlayer.name != self.name and hasSuit and card.color != suit and len(suit) > 0:
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
        print("You have removed " + str(card.value) + ", " + str(card.color) + " from your hand.")
        self.game.currentStack.append((self.name, card))

        if len(self.cards) == 0:
            return -1

#TODO: only one that sets game suit is the first player
        if self.game.leadPlayer.name == self.name:
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



import pygame
import pygame.display
import pygame.event
import pygame.draw
import random

WIN_WIDTH = 1200
WIN_WIDTH_2 = 600
WIN_HEIGHT = 900
WIN_HEIGHT_2 = 450
DOMINO_LENGTH = 96
DOMINO_WIDTH = 48
DOMINO_WIDTH_2 = 24
DOMINO_WIDTH_4 = 12
STOCK_WIDTH = 100
STOCK_HEIGHT = 50
TABLE_COLOR = (0,160,0)
LEFT = 'L'
RIGHT = 'R'
DOWN = 'D'
UP = 'U'
HAND_COUNT = 7

class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Domino:
    def __init__(self, a, b):
        self.A = a
        self.B = b
        self.isDouble = a == b

    def __eq__(self, o: object) -> bool:
        return type(o) == Domino and self.A == o.A and self.B == o.B

class Player:
    def __init__(self, id):
        self.id = id
        self.hand = []
        self.chosenDominoIndex = -1
        self.points = 0

    def takeDomino(self, domino):
        self.hand.append(domino)

class Game:
    def __init__(self):
        self._createStock()
        #self._createPlayers(playerCount)
        self.table = []
        self.playersIndex = {}
        self.players = []
        self.lastDominoLeft = None
        self.lastDominoRight = None
        self.currentPlayer = 0
        self.rightEnd = -1
        self.leftEnd = -1
        self.leftCount = 0
        self.rightCount = 0
        self.finished = False

    def _createStock(self):
        self.stock = []
        for i in range(0, 7):
            j = i
            for j in range(i, 7):
                domino = Domino(i, j)
                self.stock.append(domino)
        random.shuffle(self.stock)

    def _createPlayers(self, playerCount):
        self.playerCount = playerCount
        if self.playerCount == 1:
            player1 = Player(False)
            self.players.append(player1)
            for i in range(HAND_COUNT):
                player1.takeDomino(self.stock.pop(0))
            ai = Player(True)
            self.players.append(ai)
            for i in range(HAND_COUNT):
                ai.takeDomino(self.stock.pop(0))
        else:
            for i in range(self.playerCount):
                player = Player(False)
                self.players.append(player)
                for i in range(HAND_COUNT):
                    player.takeDomino(self.stock.pop(0))

    def getCurrentPlayer(self):
        if self.currentPlayer == len(self.players):
            self.currentPlayer = 0
        player = self.players[self.currentPlayer]
        return player

    def dominoPut(self, player: Player, domino: Domino, end):
        player.hand.remove(domino)
        self.table.append(domino)
        self.currentPlayer += 1
        if len(self.table) == 1:
            self.lastDominoLeft = domino
            self.lastDominoRight = domino
            self.leftEnd = domino.A
            self.rightEnd = domino.A
            return
        if end == LEFT:
            self.lastDominoLeft = domino
            self.leftCount += 1
            if not domino.isDouble:
                if self.leftEnd == domino.A:
                    self.leftEnd = domino.B
                else:
                    self.leftEnd = domino.A
        if end == RIGHT:
            self.lastDominoRight = domino
            self.rightCount += 1
            if not domino.isDouble:
                if self.rightEnd == domino.A:
                    self.rightEnd = domino.B
                else:
                    self.rightEnd = domino.A

    def checkPlayerCanMakeMove(self, player: Player):
        s = set()
        for d in player.hand:
            s.add(d.A)
            s.add(d.B)
        return len(s.intersection(self.leftEnd, self.rightEnd)) != 0

    def addPlayer(self, playerId):
        if len(self.players) == 4:
            return None
        player = Player(playerId)
        self.players.append(player)
        self.playersIndex[playerId] = player
        self.giveDominosToPlayer(player)
        return player

    def removePlayer(self, playerId):
        player = self.playersIndex[playerId]
        self.playersIndex.pop(playerId)
        self.players.remove(player)

    def giveDominosToPlayer(self, player):
        for i in range(HAND_COUNT):
            player.takeDomino(self.stock.pop(0))
        
    def checkGameFinished(self):
        #one of players put all dominos
        for player in self.players:
            if len(player.hand) == 0:
                return True
        #check for draw
        if self.leftEnd == self.rightEnd:
            dominosOnTableWithEnd = [d for d in self.table if d.A == self.leftEnd or d.B == self.leftEnd]
            if len(dominosOnTableWithEnd) == 7:
                return True
        return False

    def countPoints(self):
        for player in self.players:
            player.points += sum([d.A + d.B for d in player.hand])

    def newRound(self):
        self.table = []
        self._createStock()
        for p in self.players:
            p.hand = []
            p.chosenDominoIndex = -1
            self.giveDominosToPlayer(p)
        self.lastDominoLeft = None
        self.lastDominoRight = None
        self.rightEnd = -1
        self.leftEnd = -1
        self.leftCount = 0
        self.rightCount = 0
        self.finished = False
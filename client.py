from network import Network
import pygame
import pygame.display
import pygame.event
import pygame.draw
import pygame.time
import pygame.mouse
import pygame.key
import pygame.surface
import pygame.font
from game import *

pygame.init()
pygame.font.init()

FPS = 60
FONT = 'calibri'
win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
pygame.display.set_caption('Client')
n = Network()

class Placeholder:
    def __init__(self, enabled = False, x = 0, y = 0, a = 0, b = 0):
        self.enabled = enabled
        self.x = x
        self.y = y
        self.a = a
        self.b = b

    def isTouched(self, pos):
        if not self.enabled:
            return False
        x0, y0 = pos
        if x0 > self.x and x0 < self.x + self.a:
            if y0 > self.y and y0 < self.y + self.b:
                return True
        return False

    def draw(self, win):
        pygame.draw.rect(
            win, 
            (255,0,0),
            (self.x, self.y, self.a, self.b),
            width=3
        )

    def update(self, x, y, a, b):
        self.enabled = True
        self.x = x
        self.y = y
        self.a = a
        self.b = b

    def disable(self):
        self.enabled = False

#client data
placeholderFirst = Placeholder(True,
    WIN_WIDTH / 2 - DOMINO_WIDTH_2 - 6,
    WIN_HEIGHT / 2 - DOMINO_WIDTH - 6,
    DOMINO_WIDTH + 6,
    DOMINO_LENGTH + 6)
choicePlaceholder = Placeholder()
placeholderLeft = Placeholder()
placeholderRight = Placeholder()
stockPlaceholder = Placeholder(
    True,
    WIN_WIDTH_2 - STOCK_WIDTH / 2,
    0,
    STOCK_WIDTH,
    STOCK_HEIGHT
)

def redrawWindow(player, game):
    win.fill(TABLE_COLOR)
    drawTable(game)
    drawStock(game)
    drawHand(player)
    drawPlaceholders(player, game)
    pygame.display.update()

def drawSpots(win, n, coor, flow):
    if n == 0:
        return
    if n == 1:
        pygame.draw.circle(win, (0,0,0), (coor.x, coor.y), DOMINO_WIDTH / 12)
    if n == 2:
        if flow == 'R' or flow == 'L':
            pygame.draw.circle(win, (0,0,0), (coor.x - DOMINO_WIDTH_4, coor.y - DOMINO_WIDTH_4), DOMINO_WIDTH / 12)
            pygame.draw.circle(win, (0,0,0), (coor.x + DOMINO_WIDTH_4, coor.y + DOMINO_WIDTH_4), DOMINO_WIDTH / 12)
        if flow == 'D' or flow == 'U':            
            pygame.draw.circle(win, (0,0,0), (coor.x + DOMINO_WIDTH_4, coor.y - DOMINO_WIDTH_4), DOMINO_WIDTH / 12)
            pygame.draw.circle(win, (0,0,0), (coor.x - DOMINO_WIDTH_4, coor.y + DOMINO_WIDTH_4), DOMINO_WIDTH / 12)
    if n == 3:
        if flow == 'R' or flow == 'L':
            drawSpots(win, 1, coor, flow)         
            drawSpots(win, 2, coor, flow)
            pass
        if flow == 'D' or flow == 'U':   
            drawSpots(win, 1, coor, flow)         
            drawSpots(win, 2, coor, flow)
        pass
    if n == 4:
        drawSpots(win, 2, coor, 'R')
        drawSpots(win, 2, coor, 'D')
    if n == 5:
        drawSpots(win, 1, coor, flow)
        drawSpots(win, 4, coor, flow)
    if n == 6:
        drawSpots(win, 4, coor, flow)
        if flow == 'R' or flow == 'L':
            pygame.draw.circle(win, (0,0,0), (coor.x, coor.y - DOMINO_WIDTH_4), DOMINO_WIDTH / 12)
            pygame.draw.circle(win, (0,0,0), (coor.x, coor.y + DOMINO_WIDTH_4), DOMINO_WIDTH / 12)
        if flow == 'D' or flow == 'U':
            pygame.draw.circle(win, (0,0,0), (coor.x - DOMINO_WIDTH_4, coor.y), DOMINO_WIDTH / 12)
            pygame.draw.circle(win, (0,0,0), (coor.x + DOMINO_WIDTH_4, coor.y), DOMINO_WIDTH / 12)

def drawEnds(win, domino, coor: Coordinate, flow):
    if flow == 'R':
        coorA = Coordinate(coor.x - DOMINO_WIDTH / 2, coor.y)
        coorB = Coordinate(coor.x + DOMINO_WIDTH / 2, coor.y)
    if flow == 'L':
        coorA = Coordinate(coor.x + DOMINO_WIDTH / 2, coor.y)
        coorB = Coordinate(coor.x - DOMINO_WIDTH / 2, coor.y)
        pass
    if flow == 'D':
        coorA = Coordinate(coor.x, coor.y - DOMINO_WIDTH / 2)
        coorB = Coordinate(coor.x, coor.y + DOMINO_WIDTH / 2)
    if flow == 'U':
        coorA = Coordinate(coor.x, coor.y + DOMINO_WIDTH / 2)
        coorB = Coordinate(coor.x, coor.y - DOMINO_WIDTH / 2)
    drawSpots(win, domino.A, coorA, flow)
    drawSpots(win, domino.B, coorB, flow)

def drawDomino(domino):
    flow = domino.flow
    coor = domino.xy
    drawDomino(domino, coor, flow)

def drawDomino(domino, coor, flow):
    if flow == 'R' or flow == 'L':
        pygame.draw.rect(
            win, 
            (255,255,255),
            (coor.x - DOMINO_WIDTH, coor.y - DOMINO_WIDTH / 2, DOMINO_LENGTH, DOMINO_WIDTH), 
            border_radius=4)
        pygame.draw.line(
            win,
            (0,0,0),
            (coor.x, coor.y - DOMINO_WIDTH / 2),
            (coor.x, coor.y + DOMINO_WIDTH / 2))
    else: #orientation = 'V'
        pygame.draw.rect(
            win, 
            (255,255,255),
            (coor.x - DOMINO_WIDTH / 2, coor.y - DOMINO_WIDTH, DOMINO_WIDTH, DOMINO_LENGTH), 
            border_radius=4)
        pygame.draw.line(
            win,
            (0,0,0),
            (coor.x - DOMINO_WIDTH / 2, coor.y),
            (coor.x + DOMINO_WIDTH / 2, coor.y))
    drawEnds(win, domino, coor, flow)

def drawHand(player: Player):
    x = DOMINO_WIDTH
    y = WIN_HEIGHT - DOMINO_WIDTH_2 - DOMINO_WIDTH
    for d in player.hand:
        drawDomino(d, Coordinate(x, y), 'D')
        x += 3 * DOMINO_WIDTH_2

def drawPlaceholders(player: Player, game: Game):
    #first
    if len(game.table) == 0:
        placeholderFirst.draw(win)
    #choice
    if player.chosenDominoIndex != -1:
        choicePlaceholder.draw(win)
    #left
    if placeholderLeft.enabled:
        placeholderLeft.draw(win)
    #right
    if placeholderRight.enabled:
        placeholderRight.draw(win)
      
def drawTable(game: Game):
    for domino in game.table:
        drawDomino(domino, domino.xy, domino.flow)

def drawStock(game: Game):
    stock = pygame.Surface((STOCK_WIDTH, STOCK_HEIGHT))
    stock.fill((255,255,255))
    font = pygame.font.SysFont('calibri', 24, bold=True)
    text = font.render(f'Stock: {len(game.stock)}', True, (0,0,0))
    stock.blit(text, (5,10))
    win.blit(stock, (WIN_WIDTH_2 - STOCK_WIDTH / 2, 0))

def getAttachFrom(nextDomino: Domino, game: Game, end):
    attachFrom = ''
    if end == LEFT:
        attachFrom = LEFT
        if game.leftCount > 4:
            if game.leftCount == 5 and nextDomino.isDouble:
                attachFrom = LEFT
            else:
                attachFrom = UP
        if game.leftCount > 6:
            if game.leftCount == 7 and nextDomino.isDouble:
                attachFrom = UP
            else:
                attachFrom = RIGHT
    if end == RIGHT:
        attachFrom = RIGHT
        if game.rightCount > 4:
            if game.rightCount == 5 and nextDomino.isDouble:
                attachFrom = RIGHT
            else:
                attachFrom = DOWN
        if game.rightCount > 6:
            if game.rightCount == 7 and nextDomino.isDouble:
                attachFrom = DOWN
            else:
                attachFrom = LEFT
    return attachFrom

def attach(d1, d2, end, d1Coor, d1Flow, attachFrom):
    if d1.isDouble:
        #get d2 flow
        if d1Flow == 'D' or d1Flow == 'U':
            if d2.A == end:
                if attachFrom == 'R':
                    d2Flow = 'R'
                if attachFrom == 'L':
                    d2Flow = 'L'
                if attachFrom == 'D':
                    d2Flow = 'D'
                if attachFrom == 'U':
                    d2Flow = 'U'
            else:
                if attachFrom == 'R':
                    d2Flow = 'L'
                if attachFrom == 'L':
                    d2Flow = 'R'
                if attachFrom == 'D':
                    d2Flow = 'U'
                if attachFrom == 'U':
                    d2Flow = 'D'
        if d1Flow == 'R' or d1Flow == 'L':
            if d2.A == end:
                if attachFrom == 'R':
                    d2Flow = 'R'
                if attachFrom == 'L':
                    d2Flow = 'L'
                if attachFrom == 'D':
                    d2Flow = 'D'
                if attachFrom == 'U':
                    d2Flow = 'U'
            else:
                if attachFrom == 'R':
                    d2Flow = 'L'
                if attachFrom == 'L':
                    d2Flow = 'R'
                if attachFrom == 'D':
                    d2Flow = 'U'
                if attachFrom == 'U':
                    d2Flow = 'D'
        #get d2 coor
        if attachFrom == 'R':
            if d1Flow == 'D':
                d2Coor = Coordinate(d1Coor.x + DOMINO_WIDTH_2 + DOMINO_WIDTH + 1, d1Coor.y)
            else:
                d2Coor = Coordinate(d1Coor.x + DOMINO_LENGTH + 1, d1Coor.y)
        if attachFrom == 'L':
            if d1Flow == 'D':
                d2Coor = Coordinate(d1Coor.x - DOMINO_WIDTH_2 - DOMINO_WIDTH - 1, d1Coor.y)
            else:
                d2Coor = Coordinate(d1Coor.x - DOMINO_LENGTH - 1, d1Coor.y)
        if attachFrom == 'D':
            if d1Flow == 'R':
                d2Coor = Coordinate(d1Coor.x, d1Coor.y + DOMINO_WIDTH + DOMINO_WIDTH_2 + 1)
            else:
                d2Coor = Coordinate(d1Coor.x, d1Coor.y + DOMINO_LENGTH + 1)
        if attachFrom == 'U':
            if d1Flow == 'R':
                d2Coor = Coordinate(d1Coor.x, d1Coor.y - DOMINO_WIDTH_2 - DOMINO_WIDTH - 1)
            else:
                d2Coor = Coordinate(d1Coor.x, d1Coor.y - DOMINO_LENGTH - 1)
    else: #not double
        if d2.isDouble:
            #get d2 flow
            if d1Flow == 'R' or d1Flow == 'L':
                d2Flow = 'D'
            if d1Flow == 'D' or d1Flow == 'U':
                d2Flow = 'R'
            #get d2 coor
            if d1Flow == 'R' or d1Flow == 'L':
                if attachFrom == 'R':
                    d2Coor = Coordinate(d1Coor.x + DOMINO_WIDTH + DOMINO_WIDTH_2 + 1, d1Coor.y)
                if attachFrom == 'L':
                    d2Coor = Coordinate(d1Coor.x - DOMINO_WIDTH - DOMINO_WIDTH_2 - 1, d1Coor.y)
            if d1Flow == 'D' or d1Flow == 'U':
                if attachFrom == 'D':
                    d2Coor = Coordinate(d1Coor.x, d1Coor.y + DOMINO_WIDTH + DOMINO_WIDTH_2 + 1)
                if attachFrom == 'U':
                    d2Coor = Coordinate(d1Coor.x, d1Coor.y - DOMINO_WIDTH - DOMINO_WIDTH_2 - 1)
        else:
            #get d2 flow
            if d1Flow == 'R':
                if d2.A == end:
                    if attachFrom == 'R':
                        d2Flow = 'R'
                    if attachFrom == 'D':
                        d2Flow = 'D'
                    if attachFrom == 'L':
                        d2Flow = 'L'
                    if attachFrom == 'U':
                        d2Flow = 'U'
                else:
                    if attachFrom == 'R':
                        d2Flow = 'L'
                    if attachFrom == 'D':
                        d2Flow = 'U'
                    if attachFrom == 'L':
                        d2Flow = 'R'
                    if attachFrom == 'U':
                        d2Flow = 'D'
            if d1Flow == 'L':
                if d2.A == end:
                    if attachFrom == 'L':
                        d2Flow = 'L'
                    if attachFrom == 'R':
                        d2Flow = 'R'
                    if attachFrom == 'U':
                        d2Flow = 'U'
                    if attachFrom == 'D':
                        d2Flow = 'D'
                else:
                    if attachFrom == 'L':
                        d2Flow = 'R'
                    if attachFrom == 'R':
                        d2Flow = 'L'
                    if attachFrom == 'U':
                        d2Flow = 'D'
                    if attachFrom == 'D':
                        d2Flow = 'U'
            if d1Flow == 'D':
                if d2.A == end:
                    if attachFrom == 'L':
                        d2Flow = 'L'
                    if attachFrom == 'R':
                        d2Flow = 'R'
                    if attachFrom == 'D':
                        d2Flow = 'D'
                    if attachFrom == 'U':
                        d2Flow = 'U'
                else:
                    if attachFrom == 'L':
                        d2Flow = 'R'
                    if attachFrom == 'R':
                        d2Flow = 'L'
                    if attachFrom == 'D':
                        d2Flow = 'U'
                    if attachFrom == 'U':
                        d2Flow = 'D'
                    pass
            if d1Flow == 'U':
                if d2.A == end:
                    if attachFrom == 'L':
                        d2Flow = 'L'
                    if attachFrom == 'R':
                        d2Flow = 'R'
                    if attachFrom == 'D':
                        d2Flow = 'D'
                    if attachFrom == 'U':
                        d2Flow = 'U'
                else:
                    if attachFrom == 'L':
                        d2Flow = 'R'
                    if attachFrom == 'R':
                        d2Flow = 'L'
                    if attachFrom == 'D':
                        d2Flow = 'U'
                    if attachFrom == 'U':
                        d2Flow = 'D'
            #get d2Coor
            if attachFrom == 'R':
                if d1Flow == 'D' or d1Flow == 'U':
                    d2Coor = Coordinate(d1Coor.x + DOMINO_WIDTH + DOMINO_WIDTH_2 + 1, d1Coor.y - DOMINO_WIDTH_2)
                else:
                    d2Coor = Coordinate(d1Coor.x + DOMINO_LENGTH + 1, d1Coor.y)
            if attachFrom == 'D':
                if d1Flow == 'R' or d1Flow == 'L':
                    d2Coor = Coordinate(d1Coor.x + DOMINO_WIDTH_2, d1Coor.y + DOMINO_WIDTH + DOMINO_WIDTH_2 + 1)
                else:
                    d2Coor = Coordinate(d1Coor.x, d1Coor.y + DOMINO_LENGTH + 1)
            if attachFrom == 'U':
                if d1Flow == 'R' or d1Flow == 'L':
                    d2Coor = Coordinate(d1Coor.x - DOMINO_WIDTH_2, d1Coor.y - DOMINO_WIDTH - DOMINO_WIDTH_2 - 1)
                else:
                    d2Coor = Coordinate(d1Coor.x, d1Coor.y - DOMINO_LENGTH - 1)
            if attachFrom == 'L':
                if d1Flow == 'D' or d1Flow == 'U':
                    d2Coor = Coordinate(d1Coor.x - DOMINO_WIDTH - DOMINO_WIDTH_2 - 1, d1Coor.y + DOMINO_WIDTH_2)
                else:
                    d2Coor = Coordinate(d1Coor.x - DOMINO_LENGTH - 1, d1Coor.y)
    return d2Flow, d2Coor

def putFirstDomino(player: Player, game: Game):
    coor0 = Coordinate(WIN_WIDTH_2, WIN_HEIGHT_2)
    domino = player.hand[player.chosenDominoIndex]
    domino.xy = Coordinate(WIN_WIDTH_2, WIN_HEIGHT_2)
    domino.flow = 'D'
    #update player
    #player.hand.remove(domino)
    player.chosenDominoIndex = -1
    #update game
    game.dominoPut(player, domino, LEFT)
    n.makeMove(domino, LEFT)

    #drawDomino(win, domino, Coordinate(WIN_WIDTH_2, WIN_HEIGHT_2), dominoFlow)

def putDomino(player: Player, game: Game, end):
    nextDomino = player.hand[player.chosenDominoIndex]
    attachFrom = getAttachFrom(nextDomino, game, end)
    if end == LEFT:
        nextFlow, nextCoor = attach(
            game.lastDominoLeft,
            nextDomino,
            game.leftEnd,
            game.lastDominoLeft.xy,
            game.lastDominoLeft.flow,
            attachFrom)
    if end == RIGHT:
        nextFlow, nextCoor = attach(
            game.lastDominoRight,
            nextDomino,
            game.rightEnd,
            game.lastDominoRight.xy,
            game.lastDominoRight.flow,
            attachFrom)
    nextDomino.xy = nextCoor
    nextDomino.flow = nextFlow
    drawDomino(nextDomino, nextCoor, nextFlow)
    #update player
    #player.hand.remove(nextDomino)
    player.chosenDominoIndex = -1
    #update game
    game.dominoPut(player, nextDomino, end)
    n.makeMove(nextDomino, end)
    updatePlaceholders(player, game)

def canChoose(dominoIndex, player: Player, game: Game):
    d = player.hand[dominoIndex]
    if len(game.table) == 0:
        return d.isDouble
    else:
        return game.leftEnd in (d.A, d.B) or game.rightEnd in (d.A, d.B)

def updatePlaceholders(player: Player, game: Game):
    #choice
    if player.chosenDominoIndex != -1:
        choicePlaceholder.update(
        DOMINO_WIDTH_2 + (DOMINO_WIDTH_2 * 3) * player.chosenDominoIndex - 3,
        WIN_HEIGHT - DOMINO_WIDTH_2 - DOMINO_LENGTH - 3,
        DOMINO_WIDTH + 6,
        DOMINO_LENGTH + 6)
    if len(game.table) == 0:
        return
    if player.chosenDominoIndex == -1:
        placeholderLeft.disable()
        placeholderRight.disable()
        return
    domino = player.hand[player.chosenDominoIndex]
    #left
    if game.leftEnd == domino.A or game.leftEnd == domino.B:
        attachFrom = getAttachFrom(domino, game, LEFT)
        nextLeftFlow, nextLeftCoor = attach(game.lastDominoLeft, domino, game.leftEnd, game.lastDominoLeft.xy, game.lastDominoLeft.flow, attachFrom)
        x, y, a, b = 0, 0, 0, 0
        if nextLeftFlow == RIGHT or nextLeftFlow == LEFT:
            x = nextLeftCoor.x - DOMINO_WIDTH - 3
            y = nextLeftCoor.y - DOMINO_WIDTH_2 - 3
            a = DOMINO_LENGTH + 6
            b = DOMINO_WIDTH + 6
        if nextLeftFlow == DOWN or nextLeftFlow == UP:
            x = nextLeftCoor.x - DOMINO_WIDTH_2 - 3
            y = nextLeftCoor.y - DOMINO_WIDTH - 3
            a = DOMINO_WIDTH + 6
            b = DOMINO_LENGTH + 6
        placeholderLeft.update(x, y, a, b)
    else:
        placeholderLeft.disable()
    #right
    if game.rightEnd == domino.A or game.rightEnd == domino.B:
        attachFrom = getAttachFrom(domino, game, RIGHT)
        nextRightFlow, nextRightCoor = attach(game.lastDominoRight, domino, game.rightEnd, game.lastDominoRight.xy, game.lastDominoRight.flow, attachFrom)
        x, y, a, b = 0, 0, 0, 0
        if nextRightFlow == RIGHT or nextRightFlow == LEFT:
            x = nextRightCoor.x - DOMINO_WIDTH - 3
            y = nextRightCoor.y - DOMINO_WIDTH_2 - 3
            a = DOMINO_LENGTH + 6
            b = DOMINO_WIDTH + 6
        if nextRightFlow == DOWN or nextRightFlow == UP:
            x = nextRightCoor.x - DOMINO_WIDTH_2 - 3
            y = nextRightCoor.y - DOMINO_WIDTH - 3
            a = DOMINO_WIDTH + 6
            b = DOMINO_LENGTH + 6
        placeholderRight.update(x, y, a, b)
        pass
    else:
        placeholderRight.disable()

def chooseDomino(player: Player, game: Game, dominoIndex):
    player.chosenDominoIndex = dominoIndex
    updatePlaceholders(player, game)
    pass

def takeFromStock(player: Player, game: Game):
    player.hand.append(game.stock.pop(0))
    n.takeFromStock()

def click(mousePos, player: Player, game: Game):
    x, y = mousePos
    if y > WIN_HEIGHT - DOMINO_WIDTH_2 * 5 and y < WIN_HEIGHT - DOMINO_WIDTH_2:
        x0 = x - DOMINO_WIDTH_2
        if x0 > 0 and x0 < len(player.hand) * DOMINO_WIDTH_2 * 3:
            dominoIndex = x0 // (3 * DOMINO_WIDTH_2)
            if canChoose(dominoIndex, player, game):
                chooseDomino(player, game, dominoIndex)
        return
    if len(game.table) == 0:
        if placeholderFirst.isTouched(mousePos):
            putFirstDomino(player, game)
        return
    if placeholderLeft.isTouched(mousePos):
        putDomino(player, game, LEFT)
        return
    if placeholderRight.isTouched(mousePos):
        putDomino(player, game, RIGHT)
        return
    if len(game.stock) > 0 and stockPlaceholder.isTouched(mousePos):
        takeFromStock(player, game)
        return
    
def main():
    #n = Network()
    id, game = n.connect()
    n.startListen(game)
    clock = pygame.time.Clock()
    run = True
    while run:
        player = game.playersIndex[id]
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                click(pos, player, game)
        redrawWindow(player, game)

main()

def putDomino1(win, d2, end, d2Coor, d2Flow):
    nextEnd = -1
    if d2.A == d2.B:
        nextEnd = d2.A
    else:
        if d2.A == end:
            nextEnd = d2.B
        else:
            nextEnd = d2.A
    drawDomino(win, d2, d2Coor, d2Flow)
    return nextEnd

def drawtest():
    d1 = Domino(3,3)
    coor, flow, leftEnd, rightEnd = putFirstDomino(win, d1)
    rightDominoFlow = flow
    leftDominoFlow = flow
    rightDominoCoor = coor
    leftDominoCoor = coor

    d2 = Domino(3, 4)
    d2Flow, d2Coor = attach(d1, d2, leftEnd, leftDominoCoor, leftDominoFlow, 'L')
    leftEnd = putDomino1(win, d2, leftEnd, d2Coor, d2Flow)
    d3 = Domino(1, 4)
    d3Flow, d3Coor = attach(d2, d3, leftEnd, d2Coor, d2Flow, 'L')
    leftEnd = putDomino1(win, d3, leftEnd, d3Coor, d3Flow)
    d4 = Domino(1, 2)
    d4Flow, d4Coor = attach(d3, d4, leftEnd, d3Coor, d3Flow, 'L')
    leftEnd = putDomino1(win, d4, leftEnd, d4Coor, d4Flow)
    d5 = Domino(2, 6)
    d5Flow, d5Coor = attach(d4, d5, leftEnd, d4Coor, d4Flow, 'L')
    leftEnd = putDomino1(win, d5, leftEnd, d5Coor, d5Flow)
    d6 = Domino(6, 6)
    d6Flow, d6Coor = attach(d5, d6, leftEnd, d5Coor, d5Flow, 'L')
    leftEnd = putDomino1(win, d6, leftEnd, d6Coor, d6Flow)
    d7 = Domino(3, 6)
    d7Flow, d7Coor = attach(d6, d7, leftEnd, d6Coor, d6Flow, 'U')
    leftEnd = putDomino1(win, d7, leftEnd, d7Coor, d7Flow)
    d8 = Domino(3, 3)
    d8Flow, d8Coor = attach(d7, d8, leftEnd, d7Coor, d7Flow, 'U')
    leftEnd = putDomino1(win, d8, leftEnd, d8Coor, d8Flow)
    d9 = Domino(3, 4)
    d9Flow, d9Coor = attach(d8, d9, leftEnd, d8Coor, d8Flow, 'U')
    leftEnd = putDomino1(win, d9, leftEnd, d9Coor, d9Flow)
    d2 = Domino(4, 5)
    d2Flow, d2Coor = attach(d9, d2, leftEnd, d9Coor, d9Flow, 'R')
    leftEnd = putDomino1(win, d2, leftEnd, d2Coor, d2Flow)

    d2 = Domino(2, 3)
    d2Flow, d2Coor = attach(d1, d2, rightEnd, rightDominoCoor, rightDominoFlow, 'R')
    rightEnd = putDomino1(win, d2, rightEnd, d2Coor, d2Flow)
    d3 = Domino(2, 2)
    d3Flow, d3Coor = attach(d2, d3, rightEnd, d2Coor, d2Flow, 'R')
    rightEnd = putDomino1(win, d3, rightEnd, d3Coor, d3Flow)
    d4 = Domino(2, 4)
    d4Flow, d4Coor = attach(d3, d4, rightEnd, d3Coor, d3Flow, 'R')
    rightEnd = putDomino1(win, d4, rightEnd, d4Coor, d4Flow)
    d5 = Domino(4, 5)
    d5Flow, d5Coor = attach(d4, d5, rightEnd, d4Coor, d4Flow, 'R')
    rightEnd = putDomino1(win, d5, rightEnd, d5Coor, d5Flow)
    d6 = Domino(5, 5)
    d6Flow, d6Coor = attach(d5, d6, rightEnd, d5Coor, d5Flow, 'R')
    rightEnd = putDomino1(win, d6, rightEnd, d6Coor, d6Flow)
    d7 = Domino(1, 5)
    d7Flow, d7Coor = attach(d6, d7, rightEnd, d6Coor, d6Flow, 'R')
    rightEnd = putDomino1(win, d7, rightEnd, d7Coor, d7Flow)
    d9 = Domino(1, 6)
    d9Flow, d9Coor = attach(d7, d9, rightEnd, d7Coor, d7Flow, 'D')
    rightEnd = putDomino1(win, d9, rightEnd, d9Coor, d9Flow)
    d1 = Domino(3, 6)
    d1Flow, d1Coor = attach(d9, d1, rightEnd, d9Coor, d9Flow, 'D')
    rightEnd = putDomino1(win, d1, rightEnd, d1Coor, d1Flow)
    d2 = Domino(3, 5)
    d2Flow, d2Coor = attach(d1, d2, rightEnd, d1Coor, d1Flow, 'L')
    rightEnd = putDomino1(win, d2, rightEnd, d2Coor, d2Flow)
    d3 = Domino(5, 6)
    d3Flow, d3Coor = attach(d2, d3, rightEnd, d2Coor, d2Flow, 'L')
    rightEnd = putDomino1(win, d3, rightEnd, d3Coor, d3Flow)
    d4 = Domino(6, 6)
    d4Flow, d4Coor = attach(d3, d4, rightEnd, d3Coor, d3Flow, 'L')
    rightEnd = putDomino1(win, d4, rightEnd, d4Coor, d4Flow)
    d5 = Domino(5, 6)
    d5Flow, d5Coor = attach(d4, d5, rightEnd, d4Coor, d4Flow, 'L')
    rightEnd = putDomino1(win, d5, rightEnd, d5Coor, d5Flow)
    d6 = Domino(4, 5)
    d6Flow, d6Coor = attach(d5, d6, rightEnd, d5Coor, d5Flow, 'L')
    rightEnd = putDomino1(win, d6, rightEnd, d6Coor, d6Flow)
    d7 = Domino(4, 4)
    d7Flow, d7Coor = attach(d6, d7, rightEnd, d6Coor, d6Flow, 'L')
    rightEnd = putDomino1(win, d7, rightEnd, d7Coor, d7Flow)
    d8 = Domino(4, 6)
    d8Flow, d8Coor = attach(d7, d8, rightEnd, d7Coor, d7Flow, 'L')
    rightEnd = putDomino1(win, d8, rightEnd, d8Coor, d8Flow)
    d9 = Domino(2, 6)
    d9Flow, d9Coor = attach(d8, d9, rightEnd, d8Coor, d8Flow, 'L')
    rightEnd = putDomino1(win, d9, rightEnd, d9Coor, d9Flow)
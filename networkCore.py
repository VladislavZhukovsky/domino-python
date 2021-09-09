class ClientAction:
    def __init__(self, playerId):
        self.playerId = playerId

        self.move = False
        self.domino = None
        self.end = None

        self.takeFromStock= False

class GameInfo:
    def __init__(self):
        #player
        #table
        #stock
        pass
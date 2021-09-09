import socket
import pickle
import networkCore
import threading
import game

FORMAT = 'utf-8'
HEADER = 2048

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.100.16"
        self.port = 5555
        self.addr = (self.server, self.port)

    def connect(self):
        try:
            self.client.connect(self.addr)
            clientId = self.client.recv(HEADER).decode(FORMAT)
            self.clientId = clientId
            print(clientId)
            gameInfoString = self.client.recv(HEADER)
            print(gameInfoString)
            gameInfo = pickle.loads(gameInfoString)
            return clientId, gameInfo
        except:
            pass

    def startListen(self, clientGame: game.Game):
        thread = threading.Thread(target=handle, args=(self.client, clientGame))
        thread.start()

    def makeMove(self, domino: game.Domino, end: str):
        action = networkCore.ClientAction(self.clientId)
        action.move = True
        action.domino = domino
        action.end = end

        actionStr = pickle.dumps(action)
        self.client.send(actionStr)

    def takeFromStock(self):
        action = networkCore.ClientAction(self.clientId)
        action.takeFromStock = True
        actionStr = pickle.dumps(action)
        self.client.send(actionStr)

def handle(client: Network, clientGame: game.Game):
    while True:
        try:
            msg = client.recv(HEADER)
            obj = pickle.loads(msg)
            if type(obj) == game.Game:
                clientGame.table = obj.table
                clientGame.stock = obj.stock
                clientGame.players = obj.players
                clientGame.playersIndex = obj.playersIndex
                clientGame.lastDominoLeft =  obj.lastDominoLeft
                clientGame.lastDominoRight =  obj.lastDominoRight
                clientGame.currentPlayer =  obj.currentPlayer
                clientGame.rightEnd =  obj.rightEnd
                clientGame.leftEnd =  obj.leftEnd
                clientGame.leftCount =  obj.leftCount
                clientGame.rightCount =  obj.rightCount
                clientGame.finished =  obj.finished
        except WindowsError:
            print(f'Error - Server connection lost')
            exit()
import socket
import threading
import pickle
import game as DominoGame
import networkCore

PORT = 5555
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
HEADER = 2048

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
clients = {}
game = DominoGame.Game()

def clientJoins():
    conn, addr = server.accept()
    thread = threading.Thread(target=handle, args=(conn, addr))
    thread.start()
    print(f'[Active collections]: {threading.active_count() - 1}')
    #for client in clients:
        #clients[client].send(f'Client {clientId} connected'.encode(FORMAT))

def notifyAll():
    gameStr = pickle.dumps(game)
    for client in clients.values():
        client.send(gameStr)

def handle(client: socket.socket, addr):
    #player connects
    clientId = str(addr[1])
    clients[clientId] = client
    print(f'Joined user: {clientId} Number of users: {len(clients)}')
    client.send(f'{clientId}'.encode(FORMAT))
    game.addPlayer(clientId)
    notifyAll()
    connected = True
    while connected:
        try:
            objStr = client.recv(HEADER)
            obj = pickle.loads(objStr)
            if type(obj) == networkCore.ClientAction:
                if obj.move:
                    game.dominoPut(game.playersIndex[clientId], obj.domino, obj.end)
                    finished = game.checkGameFinished()
                    if finished:
                        game.countPoints()
                        game.newRound()
                if obj.takeFromStock:
                    player = game.playersIndex[clientId]
                    player.hand.append(game.stock.pop(0))
            notifyAll()
        except WindowsError:
            print(f'Error - Client {clientId} disconnected')
            connected = False
            clients.pop(clientId)
            game.removePlayer(clientId)
            game.newRound()
            notifyAll()
    client.close()
    print(f'[DISCONNECTED]: {addr}') 

def start():
    server.listen()
    while True:
        clientJoins()

print('[Starting Domino server...]')
start()
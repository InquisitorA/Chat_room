import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 55555))
server.listen()

clients = []
usernames = []
serverdata = {}

def broadcast(message):
    for client in clients:
        client.send(message)
        
def unicast(client, message):
    client.send(message)

def handle(client):
    while True:
        for key, value in serverdata.items():
         if client == value:
             username = key
        try:
            message = client.recv(1024).decode('ascii')
            info = message.split(' ', 1)
            if info[0][0] == "@":
                recipient = info[0][1:len(info[0])]
                if recipient in serverdata.keys():
                    recvclient = serverdata[recipient]
                    ucmessage = username + ': ' + info[1]
                    recvmessage = ucmessage.encode('ascii')
                    unicast(recvclient, recvmessage)
                elif recipient == 'all':
                    bcmessage = username + ': ' + info[1]
                    broadcast(bcmessage.encode('ascii'))
                else:
                    client.send('Requested user does not exist'.encode('ascii')) 
            else:
                client.send('Invalid message'.encode('ascii'))

        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            username = usernames[index]
            broadcast((username + ' has left the server!').encode('ascii'))
            print(username + ' has left the server!')
            usernames.remove(username)
            break
            

def receive():
    while True:
        client, address = server.accept()

        client.send('ack'.encode('ascii'))
        username = client.recv(1024).decode('ascii')
        
        valid = username.isalnum()
        
        if valid == True:
            usernames.append(username)
            clients.append(client)
            serverdata[username] = client
            
            print(username + ' registered on the server')
            client.send('You are now connected to the server!'.encode('ascii'))
        
        else:
            client.send('Invalid username'.encode('ascii'))

        thread = threading.Thread(target = handle, args = (client,))
        thread.start()

receive()
import socket
import threading

# Connection Data
host = '127.0.0.1'
port = 55555

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)

# Lists For Clients and Their Nicknames
clients = []
nicknames = []
name_clients = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            msg = message = client.recv(1024)
            if msg.decode('ascii').startswith('KICK'):
                name_to_kick = msg.decode('ascii')[5:]
                kick_user(name_to_kick)

            elif msg.decode('ascii').startswith('BAN'):
                name_to_ban = msg.decode('ascii')[4:]
                kick_user(name_to_ban)

            else:
                broadcast(message)

        except:
            index = client.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast("system: %s ha abbandonato la chat".encode('ascii') % nickname)
            nicknames.remove(nickname)
            break

def recive():
    while True:
        client, address = server.accept()
        print "connesso con", str(address)
        
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')

        if nickname[0].startswith('ADMIN_'):
            client.send('PASS'.encode('ascii'))
            password = client.recv(1024).decode('ascii')
            if password != "adminpass":
                client.send('REFUSE'.encode('ascii'))
                client.close()
                continue
            else:
                client.send('CORRECT'.encode('ascii'))


        client.send('CLIENT'.encode('ascii'))
        name_client = client.recv(1024).decode('ascii')

        nicknames.append(nickname)
        clients.append(client)
        name_clients.append(name_client)

        print "il soprannome di", str(name_client), "e'", str(nickname)
        broadcast("server: %s si e' unito alla chat".encode('ascii') % nickname)
        client.send("connesso con il server".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print "in cerca di utenti online..."
recive()
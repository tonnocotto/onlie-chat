import socket
import threading

prompt = '> '
host = "127.0.0.1"
nickname = ""
name_client = socket.gethostname()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print "\ninserisci un nickname:"

while (len(nickname) > 10) or (len(nickname) == 0):
    nickname = raw_input(prompt)
    if nickname == "":
        nickname = name_client
        break
    elif nickname[0].startswith("ADMIN_"):
        print "inserisci la password:"
        password = raw_input(prompt)

        if ((len(nickname) - 6) < 10) or ((len(nickname) - 6) == 10):
            continue

client.connect(("127.0.0.1", 55555))

stop_thread = False

def receive():
    while True:
        global stop_thread
        if stop_thread == True:
            break
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
                if nickname[0].startswith("ADMIN_"):
                    nex_message = client.recv(1024).decode('ascii')
                    if nex_message == 'PASS':
                        client.send(password.encode('ascii'))
                        if client.recv(1024).decode('ascii') == 'REFUSE':
                            print "password errata"
                            stop_thread = True
                        else:
                            print "password corretta"

            elif message == 'CLIENT':
                client.send(name_client.encode('ascii'))
            elif message == "server: %s si e' unito alla chat" % nickname:
                pass
            else:
                print(message)
        except:
            # Close Connection When Error
            print("si e' verificato un'errore!")
            client.close()
            break

def write():
    while True:
        if stop_thread == True:
            break

        message_c = raw_input()
        message = nickname + ": " + message_c + "\n"
        if message[len(nickname)+2:].startswith('/'):
            if nickname.startswith("ADMIN_"):

                if message[len(nickname)+2:].startswith('/kick'):
                    client.send('KICK %s'.encode('ascii') % message[len(nickname)+2+6:])

                elif message[len(nickname)+2:].startswith('/ban'):
                    client.send('BAN %s'.encode('ascii') % message[len(nickname)+2+5:])
            else:
                print "i comandi sono eseguibili solo dagli admin"

        else:
            client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

whrite_thread = threading.Thread(target=write)
whrite_thread.start()
import socket
import threading
import queue
import time

# Vi laver en tom liste, som skal indeholde alle vores clients
clients = []

# Vi laver en queue, som skal indeholde alle beskederne
messages = queue.Queue()

# Vi sætter IP-adresse og portnr. til to variabler
host = "127.0.0.1"
port = 9000

# Vi sætter en socket op. AF_INET betyder at IP-adresse familien er IPv4, og SOCK_STREAM betyder, at det er TCP
connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vi binder vores socket til IP-adresse og port
connection.bind((host,port))

# Denne funktion lytter på vores connection
connection.listen(10)

# Denne funktion accepterer forbindelsen
def acceptConnections():
   # Vi sætter nicknames til 0
   names = 0
   while True:
       conn, addr = connection.accept()
       client_dict = {"NICKNAME": names, "HEARTBEAT": time.time(), "CLIENT": conn}
       clients.append(client_dict)
       names += 1
       print("New client joined the chat", addr)
       t = threading.Thread(target=client_thread, args=(conn,))
       t.start()


def broadcast_messages():
    while True:
        msg = messages.get()
        for c in clients:
            c["CLIENT"].send(msg.encode())


def client_thread(conn):
    while True:
        msg = conn.recv(1024).decode()
        messages.put(msg)
        print("Message from client: ", msg)


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(bufferSize).decode()
    welcome = 'Welcome %s! Type quit to exit the chat.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast_messages(bytes(msg, "utf8"))
    clients[client] = name

    while True:
        msg = client.recv(bufferSize)
        if msg != bytes("quit", "utf8"):
            broadcast_messages(msg, name+": ")
        else:
            client.send(bytes("quit", "utf8"))
            client.close()
            del clients[client]
            broadcast_messages(bytes("%s has left the chat." % name, "utf8"))
            break


bufferSize = 1024

threading.Thread(target=broadcast_messages).start()

acceptConnections()
handle_client(connection)


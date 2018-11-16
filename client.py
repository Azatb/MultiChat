import socket
from tkinter import *
import threading


def sendMessage():
    mySocket.send(entryField.get().encode())

def receiveMessage():
    while True:
        data = mySocket.recv(1024).decode()
        print(data)
        listBoxOfChatMessages.insert(END, data)
        listBoxOfChatMessages.see(END)

host = '127.0.0.1'
port = 9000

mySocket = socket.socket()
mySocket.connect((host, port))


root = Tk()
root.geometry("600x400")

bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)

sendMessage = Button(bottomFrame, text="Send besked", fg="red", command=sendMessage)
sendMessage.pack()

entryField = Entry(bottomFrame)
entryField.pack()

listBoxOfChatMessages = Listbox(root, height=30, width=75)
listBoxOfChatMessages.pack(side=TOP)


t = threading.Thread(target=receiveMessage)
t.start()

root.mainloop()

mySocket.close()



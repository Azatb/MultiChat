import socket
from tkinter import *
from tkinter import messagebox
import threading


class Client:

    def __init__(self, root):
        self.root = root
        self.root.title("Your nickname")

        self.my_frame = Frame(self.root)
        self.name = ""
        self.nickname = StringVar()

        self.nickname.set("")
        enter_nickname = Entry(self.my_frame, textvariable=self.nickname)

        enter_nickname.pack(fill=X)

        send_button = Button(self.my_frame, text="Enter desired nickname", command=self.toggle_chat, bg="green", fg="black")
        send_button.pack()
        self.my_frame.grid(column=0, row=0)

    def toggle_chat(self):
        self.name = self.nickname.get()
        self.root.title("Mathias' chat")
        self.my_frame.grid_remove()
        messages_frame = Frame(self.root)
        scrollbar = Scrollbar(messages_frame)
        global msg_list
        msg_list = Listbox(messages_frame, bg="lightblue", height=30, width=60, yscrollcommand=scrollbar.set)

        # To see through previous messages.
        scrollbar.pack(side=RIGHT, fill=Y)
        msg_list.pack(side=LEFT, fill=BOTH)
        msg_list.pack()

        messages_frame.pack()
        global my_msg
        my_msg = StringVar()

        entry_field = Entry(self.root, textvariable=my_msg)

        my_msg.set(entry_field.get())

        entry_field.bind("<Return>", func=lambda f: self.send_message())
        entry_field.pack(fill=X)

        send_msg_button = Button(self.root, text="Send message", command=self.send_message, bg="green", fg="black")
        send_msg_button.pack()
        change_nickname_field = Entry(self.root, textvariable=self.nickname)
        change_nickname_field.pack(fill=X)

        change_nickname_btn = Button(self.root, text="Change your Nickname", command=lambda: self.change_nickname(self.nickname),
                                    bg="green", fg="black")
        change_nickname_btn.pack()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        receive_thread = threading.Thread(target=self.receive_message)
        receive_thread.start()

    def change_nickname(self, nickname):
        self.name = nickname.get()
        messagebox.showinfo("Just changed your nickname", "You have changed your nickname to: " + nickname.get())

    def on_closing(self):
        """This function is to be called when the window is closed."""
        my_msg.set("quit")
        self.send_message()
#
    def send_message(self):
        global my_msg
        msg = my_msg.get()
        message_to_be_sent = self.name + ": " + msg
        sock.send(message_to_be_sent.encode())
        if msg == "quit":
            sock.close()
            self.root.quit()

    @staticmethod
    def receive_message():
        while True:
            try:
                msg = sock.recv(1024).decode()
                print(msg)
                msg_list.insert(END, msg)
                msg_list.see(END)
            except OSError:
                break


host = "127.0.0.1"
port = 9000

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

start_window = Tk()
client = Client(start_window)
start_window.mainloop()

# Vi skal lave sådan, at andre brugere kan se, at man ændrer sit nickname
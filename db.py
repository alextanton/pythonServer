from pymongo import MongoClient
import Connection

class DB:
    def __init__(self):
        self.collection = MongoClient().local.connections

    def REMOVEALL(self):
        self.collection.delete_many({})

    def remove(self, connection, field):
        if("ip" in field):
            self.collection.delete_many({"ip": connection.ip})
        elif("hostname" in field):
            self.collection.delete_many({"hostname": connection.hostname})
        elif("socket" in field):
            self.collection.delete_many({"socket": str(connection.socket)})
        elif(True):
            return False
        return True

    def insert(self, connection):
        self.collection.insert_one({
            "ip": connection.ip,
            "hostname": connection.hostname,
            "socket": str(connection.socket)
        })

    def find(self, connection):
        self.collection.find({"ip": connection.ip,
            "hostname": connection.hostname,
            "socket": str(connection.socket)})

    def getConnectionHostIP(self, ip, hostname):
        c = self.collection.find({"ip": ip,
            "hostname": hostname})
        c = Connection.Connection(c["ip"], c["hostname"], c["socket"])
        return c

    def findBySock(self, socket):
        c = self.collection.find({"socket": socket})
        c = Connection.Connection(c["ip"], c["hostname"], c["socket"])

    def getAllConnectionsPrint(self):
        darr = []
        docs = self.collection.find()
        for doc in docs:
            darr.append(doc)
        return darr

    def getCollection(self):
        return self.collection
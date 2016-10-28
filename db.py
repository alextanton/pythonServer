from pymongo import MongoClient

class DB:
    def __init__(self):
        self.collection = MongoClient().local.connections

    def remove(self, connection, field):
        if("ip" in field):
            self.collection.delete_many({"ip": connection.ip})
        elif("hostname" in field):
            self.collection.delete_many({"hostname": connection.hostname})
        elif("socket" in field):
            self.collection.delete_many({"socket": connection.socket})
        elif(True):
            return False
        return True

    def insert(self, connection, field):
        self.collection.insert_one({
            "ip": connection.ip,
            "hostname": connection.hostname,
            "socket": connection.socket
        })

    def find(self, connection):
        self.collection.find({"ip": connection.ip,
            "hostname": connection.hostname,
            "socket": connection.socket})
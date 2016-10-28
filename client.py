from pymongo import MongoClient

client = MongoClient()

db = client.test
coll = db.test

coll.insert_one({
    "name": {
        "first": "alex",
        "last": "tanton",
    },
    "age": 22
})

def main():
    cur = coll.find()
    for doc in cur:
        print(doc)

main()
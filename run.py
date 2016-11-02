import server
import client
import Connection

def main():
    cli = client.Client()
    cli.DB.REMOVEALL()
    ser = server.Server(cli)
    cli.createWindow()
    #c = Connection.Connection("ip", "host", "asdfasd")
    #cli.DB.insert(c)

main()
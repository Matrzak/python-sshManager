import json
import sys
import os

allConnection = []

class Connection:
        def __init__(self,name,host,user,password):
                self.name = name
                self.host = host
                self.user = user
                self.password = password
                allConnection.append(self)

def manageCommand(command):
    splited = command.split(' ')
    command = splited[0]
    del splited[0]
    if command == "save":
        saveCommand(splited)
    if command == "quit":
            sys.exit(0)
    if command == "connect":
            connectCommand(splited)

def getConnectionByName(name):
        for connection in allConnection:
                if connection.name == name:
                        return connection


def connectCommand(args):
        connection = getConnectionByName(args[0])
        if connection is None:
                return
        os.system("sshpass -p "+connection.password+" ssh "+connection.user+"@"+connection.host)

def saveCommand(args):
    exists = 0
    for connection in allConnection:
        if connection.name == args[0]:
            exists = 1

    if exists == 1:
        print("SSH connection with this name already exists")
        return

    values = {
        "name": args[0],
        "host": args[1],
        "user": args[2],
        "password": args[3]
    }
    Connection(args[0],args[1],args[2],args[3])
    x = json.dumps(values)
    saveNewLine(x)

def saveNewLine(json):
    with open("settings.json", "a") as f:
        f.write(json+"\n")
        f.close()

def loadSettings():
    try:
        with open("settings.json") as f:
            for line in f:
                x = json.loads(line)
                Connection(x["name"], x["host"], x["user"], x["password"])
    except:
        file = open("settings.json", "w+")
        file.close()
        print("Settings file not found, creating one")

def runCommandHandler():
    while True:
        value = input("Type your command\n")
        manageCommand(value)

loadSettings()
runCommandHandler()

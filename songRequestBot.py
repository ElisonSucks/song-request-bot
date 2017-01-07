import socket
import string

# -- Dont mess with these settings --
HOST = "irc.twitch.tv"
PORT = 6667
songList = []
songListName = []

# -- Mess with these... --
BOTNAME = "" #Bots name
BOT_OAUTH = "oauth:" #Bots OAuth
CHANNEL = "" #Connecting channel
moderators = [CHANNEL]

# -- DO NOT MESS WITH ANYTHING BELOW !!! ---
s = socket.socket()
s.connect((HOST, PORT))
s.send(bytes("PASS " + BOT_OAUTH + " \r\n", "utf-8"))
s.send(bytes("NICK " + BOTNAME + " \r\n", "utf-8"))
s.send(bytes("JOIN #" + CHANNEL + " \r\n", "utf-8"))

def request(user, msg):
    print(songListName)
    if songListName.count(user) > 1:
        sendMsg("@" + user + " you are only allowed two requests...")
    else:
        sendMsg("@" + user + " requested " + msg[5:(len(msg))] + "!")
        songList.append([user,msg[5:]])
        songListName.append(user)
                
def chatPriv(user, msg):
    global moderators

    if user in moderators:
        commands(user, msg, 1)
    else:
        commands(user, msg, 0)

def commands(user, msg, priv):
    def chatCommands(user, msg):
        if msg[0:6] == "!song ":
            request(user, msg)

    if priv == 1:
        print('mod')
        chatCommands(user,msg)
    else:
        chatCommands(user,msg)

def sendMsg(msg):
    temp = bytes("PRIVMSG #" + CHANNEL + " :" + msg + "\r\n", "utf-8")
    s.send(temp)

while True:
    line = str(s.recv(1024))
    if "End of /NAMES list" in line:
        break

while True:

    tempSpace = str(s.recv(1024)).split('\\r\\n')

    for line in tempSpace:
        parts = line.split(':')
        if len(parts) < 3:
            continue

        if "QUIT" not in parts[1] and "JOIN" not in parts[1] and "PART" not in parts[1]:
            message = parts[2][:len(parts[2])]

        username = (parts[1].split("!"))[0]
        if message[0] == "!":
            chatPriv(username, message)
        

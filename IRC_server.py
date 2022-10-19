import platform
import socket
from threading import Thread

# Global variables, used to store the server's IP address and port number
#socket creation
serversocket = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
host = ""
port = 6667
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
    # Bind the socket to the host and port
    serversocket.bind((host, port))
    if platform.system() == "Windows":
        print("Server started on Windows")
    elif platform.system() == "Linux":
        print("Server started on Linux")
    elif platform.system() == "Darwin":
        print("Server started on Mac")
    else:
        print("Server started on unknown OS")
except socket.error as e:
    print(e)

client_list = []
channel_list = []
banned_users = []


# The client class that handles the client's connection
class client(Thread):
    # Constructor for the client class
    def __init__(self, socket, address):
        Thread.__init__(self)
        self.sock = socket
        self.addr = address
        self.nickname = ""
        self.user = ""
        self.channel = []
        self.start()

    def run(self):
        #ensure that all login information is received before continuing
        try:
            #While username and nickname not set
            while self.nickname == "" and self.user == "":              
                while self.user == "":
                    # Read received data from the client
                    message = self.sock.recv(1024).decode()
                    for line in message.splitlines():
                        messageParsed = line.split(' ')
                        # Check if the client is sending a nickname parameter to the server
                        if(messageParsed[0] == "NICK"):
                            global client_list
                            if(messageParsed[1] != ""):
                                #if the nickname is admin, ask for password
                                if messageParsed[1] == "admin":
                                    self.sock.send(b'Password: ')
                                    #nb: 2**10 is the max size of a message
                                    password = self.sock.recv(1024).decode()
                                    if password == "admin":                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 
                                        self.nickname = messageParsed[1]
                                    elif password == "admin" and messageParsed[1] in client_list:
                                        self.sock.send(b'Nickname is already in use')
                                        self.sock.close()
                                        return
                                    else:
                                        self.sock.send(b'Incorrect password')
                               
                                for client in client_list:
                                    # inform user if the nickname already exist
                                    if messageParsed[1] == client.nickname:
                                        message = self.nickname + ' ' + messageParsed[1] + ':Nickname is already in exists\n'
                                        self.sock.send(message.encode())
                                        self.sock.close()
                                        return
                                self.nickname = messageParsed[1]
                            else:
                                self.sock.send(b'Error: Please enter a nickname')

                        # Check if the client is sending a username parameter
                        if(messageParsed[0] == "USER"):
                            if(messageParsed[1] != ""):
                                self.user = messageParsed[1]
                            else:
                                self.sock.send(b'Error: Please enter a username')
             
            print(self.user + " has joined the server" + " with the nickname " + self.nickname)
            if(self.nickname != "" and self.user != ""):
                print("Adding " + self.user + " to client list...")
                try:
                    client_list.append(self)
                    print("Client list updated")
                except:
                    print("Error: Could not add client to client list")

                # Constructing and sending the initial welcome messages
                msg1 = ':' + host + ' 001 ' + self.nickname + ' :Welcome to Group_10 server!\n'
                message = msg1 + "Join general by typing /join #test\n"
                                
                self.sock.send(message.encode())
  
            while True:

                message = self.sock.recv(1024).decode()
                for line in message.splitlines():
                    messageParsed = line.split(' ')

                

                    #Join a channel if it exists and the user is not banned

                    if(messageParsed[0] == "JOIN"):
                        found = False
                        for channel in channel_list:
                            if(messageParsed[1] in banned_users):
                                self.sock.send(b'You are banned from this channel\n')
                                break
                            if(messageParsed[1] == channel):
                                found = True                 
                        channel = messageParsed[1]

                        #If channel not found, create channel with name
                        if(not found):
                            channel_list.append(channel)
                            found = True

                        #If channel found, send reply codes and broadcast to everyone in channel
                        if (found):
                            #200 and 300 are reply codes,that the server uses to inform the client that the command was successful
                            self.channel.append(channel)
                            chmsg1 = ':' + host + ' 200 ' + self.nickname + ' ' + channel + ' :No topic is set\n'
                            chmsg2 = ':' + host + ' 300 ' + self.nickname + ' = ' + channel + ' :'
                            inforserver = "NICK: " + self.nickname + " USERNAME: " + self.user + ' @ ' + self.addr[0] + '\n' + platform.node() + ' JOINED ' + channel + '\n'

                            #Add every client in channel to list of users in channel 
                            for client in client_list:
                                for clientChannel in client.channel:
                                    if(clientChannel == channel):
                                        chmsg2 = chmsg2 + ' ' + client.nickname
                            chmsg2 = chmsg2 + '\n'

                            #Send channel reply codes 
                            chan_list = ':' + host + ' 366 ' + self.nickname + ' ' + channel + ' :End of NAMES list\n'
                            REPLY = ':' + self.nickname + "!" + self.user + '@' + platform.node() + ' ' + line + '\n'
                            message = REPLY + chmsg1 + chmsg2 + chan_list
                            servermsg = inforserver + chmsg1
                            print(servermsg)

                            #send a message to clients in the channel
                            for client in client_list:
                                for clientChannel in client.channel:
                                    if(clientChannel == channel):
                                        client.sock.send(message.encode())

                    #Leave channel protocol
                    if(messageParsed[0] == "PART"):
                        if(self.channel):
                            channel = messageParsed[1]
                            message = ':' + self.nickname + "!" + self.user + '@' + platform.node() + ' ' + line + '\n'
                            #For each client in channel, send message that user left
                            for client in client_list:
                                for clientChannel in client.channel:
                                    if(clientChannel == channel):
                                        client.sock.send(message.encode())
                            #Remove channel frm users channel list
                            self.channel.remove(channel)
                            print(self.nickname + " left " + channel)

                    #Leave server
                    if(messageParsed[0] == "QUIT"):
                        #For each client, send message that user has quit
                        for client in client_list:
                            message = ':' + self.nickname + "!" + self.user + '@' + platform.node() + ' ' + line + '\n'
                            client.sock.send(message.encode())
                        #Remove user from list of clients and then close the socket
                        client_list.remove(self)
                        print(self.nickname + " has quit")
                        self.sock.close()

                    #Message protocol
                    if(messageParsed[0] == "PRIVMSG"):
                        channel = messageParsed[1]
                        for client in client_list:
                            
                            #Message Channel
                            for clientChannel in client.channel:
                                if(clientChannel == channel):
                                    if (client != self):
                                        message = ':' + self.nickname + "!" + self.user + '@' + platform.node() + ' ' + line + '\n'
                                        client.sock.send(message.encode())


                            #Message Users privately
                            #correctly formats to send a private message to a user is correct format is /msg <nickname> <message>          
                            if(messageParsed[1] == client.nickname):
                                if(messageParsed[2] != ":"):
                                    if(messageParsed[1] != self.nickname):
                                        message = ':' + self.nickname + "!" + self.user + '@' + platform.node() + ' ' + line + '\n'
                                        client.sock.send(message.encode())
                                        print(self.nickname + " sent a private message to " + client.nickname)

                    #List all users in channel
                    if(messageParsed[0] == "NAMES"):
                        channel = messageParsed[1]
                        message = ':' + host + ' 353 ' + self.nickname + ' = ' + channel + ' :'
                        for client in client_list:
                            for clientChannel in client.channel:
                                if(clientChannel != channel):
                                    message = "Join channel to see users!"
                                if(clientChannel == channel):
                                    message = message + client.nickname + ' '
                        message = message + '\n' + ':' + host + ' 366 ' + self.nickname + ' ' + channel + ' :End of NAMES list\n'
                        print(self.nickname + " requested a list of users in " + channel)
                        self.sock.send(message.encode())


                    #user priviledges protocol
                    if(messageParsed[0] == "KICK"):
                        if(self.user == "admin"):
                            channel = messageParsed[1]
                            for client in client_list:   
                               if(messageParsed[2] == client.nickname):
                                    message = ':' + self.nickname + "!" + self.user + '@' + platform.node() + ' ' + line + '\n'
                                    client.sock.send(message.encode())
                                    print(self.nickname + " kicked " + client.nickname + " from " + channel)
                                    client.channel.remove(channel)
                            for client in client_list:
                                for clientChannel in client.channel:
                                    if(clientChannel == channel):
                                        message = ':' + self.nickname + "!" + self.user + '@' + platform.node() + ' ' + line + '\n'
                                        client.sock.send(message.encode())
                        else:
                            message = ':' + host + ' 481 ' + self.nickname + ' :Permission Denied- You do not have access to this command\n'
                            self.sock.send(message.encode())

                    #admin  can be able to ban a user from a channel, names of users banned from a channels are added to a banned users and cannot rejoin
                    if(messageParsed[0] == "BAN"):
                        if(self.user == "admin"):
                            channel = messageParsed[1]
                            for client in client_list:
                                if(messageParsed[2] == client.nickname):
                                    message = ':' + self.nickname + "!" + self.user + '@' + platform.node() + ' ' + line + '\n'
                                    client.sock.send(message.encode())
                                    print(self.nickname + " banned " + client.nickname + " from " + channel)
                                    banned_users.append(client.nickname)
                                    client.channel.remove(channel) 
                            for client in client_list:
                                for clientChannel in client.channel:
                                    if(clientChannel == channel):
                                        message = ':' + self.nickname + "!" + self.user + '@' + platform.node() + ' ' + line + '\n'
                                        client.sock.send(message.encode())
                        else:
                            message = ':' + host + ' 481 ' + self.nickname + ' :Permission Denied- You do not have access to this command\n'
                            self.sock.send(message.encode())        

        except socket.error as e:
            print("Error: " + str(e))
            client_list.remove(self.sock)
            self.sock.close()

#Listen for client connections to server
serversocket.listen(5)
print("Server is running and listening on port " + str(port))

while True:
    clientsocket, address = serversocket.accept()
    client(clientsocket, address)
        
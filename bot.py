#!/bin/python3

# imports

from email import message
import Bot_commands as commands
import socket as s
import sys
import os
import random as rand

#main class for the bot
class bot():
    #instanciate variables
    def __init__(self, server, channel, name, nickname):
        self.server=server
        self.channel=channel
        self.name=name
        self.nickname=nickname
        self.sock=s.socket(s.AF_INET, s.SOCK_STREAM)
        self.host_ip=s.gethostbyname(s.gethostname())
        self.user_list=[]
        self.connect_to_server()
        self.join_channel(self.channel)
        #conect to server
    def connect_to_server(self):
        #try connecting to server and if it fails, print error and exit
        try:
            self.sock.connect((self.server, 6667))
            print(f"connected to {self.host_ip}")
            self.sock.send(bytes("USER "+self.nickname+" "+self.nickname+" "+self.nickname+" :"+self.nickname+"\r\n", "UTF-8"))
            self.sock.send(bytes("NICK "+self.name+"\r\n", "UTF-8"))
        except s.error as e:
            print(f"Error: {str(e)} unable to connect to server")
            sys.exit()
            
    """Join channel function receives two inputs the channel name and the socket"""
    
    def join_channel(self, channel_name):
        #if channel is empty print to console channel empty and exit
        if channel_name=="":
            print("Error: channel name is empty")
            sys.exit(-1)
            
            #else try joining channel if failed print error and close socket
        else:
            try:
                self.sock.send(bytes("JOIN "+channel_name+"\r\n", "UTF-8"))
                print("joined channel "+channel_name)
                self.sock.send(bytes("PRIVMSG "+channel_name+" :Hello, I am a"+self.nickname+" !\r\n", "UTF-8"))
            except s.error as e:
                print("Error: "+str(e)+"unable to join channel")
                s.close()
                
      
    #send message function
    # receives the socket, destination and message as inputs then send the message to the required channel or destination
    def send_message(self,dest, message):
        #if destination is empty print error and exit
        if dest=="":
            print("Error: destination is empty")
            sys.exit(-2)
            #if message is empty print error and exit
        if message=="":
                print("Error: message is empty")
                sys.exit(-3)
                #else try sending message if failed print error and close socket
        else:
            try:
                self.sock.send(bytes("PRIVMSG "+dest+" :"+message+"\r\n", "UTF-8"))
            except s.error as e:
                print("Error: "+str(e)+"unable to send message")
                s.close()     
                   
    def  get_user(self,data):
        user=data.split()
        user=user[0].strip(":")
        return user
    def add_user(self,user):
        self.user_list.append(user)
        return self.user_list
    
    def remove_user(self,user):
        self.user_list.remove(user)
        return self.user_list
    
    def main(self):
                    
                      
        #while loop to handle connection, sending of messages and receiving of messages
        while True:
            
            
            #try receiving messages from server if failed print error and close socket
            try:
                data=self.sock.recv(1024).decode("UTF-8")
                
                if data.find("PING")!=-1:
                    self.sock.send(bytes("PONG "+data.split()[1]+"\r\n", "UTF-8"))
                    
                #keep track of users in channel who JOIN
                if data.find("JOIN")!=-1:
                  user=self.get_user(data)
                  addu=self.add_user(user)
                  print("user joined: "+user)
              #Keep track of users in channel who PART
                elif data.find('!QUIT')!=-1:
                    us=self.get_user(data)
                    remov=self.remove_user(us)
                    print("user left: "+us)
               
               #respond to messages in channel
                #respond hello
                #provide help
                #roll a dice
                #slap a user
                if data.find("PRIVMSG")!=-1:
                    message=data.split("PRIVMSG",1)[1].split(":",1)[1]
                    print(message)
                    if message.startswith("!"):
                        if message.startswith("!hello"):
                            self.send_message(channel, "Hello")
                        elif message.startswith("!help"):
                            self.send_message(channel, "Commands: !hello, !help, !roll, !slap")
                        elif message.startswith("!roll"):
                            diceroll=rand.randint(1,6)
                            self.send_message(channel, f"You rolled a {diceroll}")
                        elif message.startswith("!slap"):
                            randuser=rand.choice(self.user_list)
                            self.send_message(channel,"slaps"+randuser+"with a large trout \n")
                           
                           
                        """   #respond to private messagees
                           usr=message[0].strip(":")
                        elif message.find("PRIVMSG"+usr) != -1:
                          print(f"received a private message from {usr}")
                          msg=rand.choice(list(open("facts.txt")))
                          self.send_message(usr, "msg")
                        """
                    else :
                        bot_replies.random_replies()  
                   
            except s.error as e:
                print("Error: "+str(e)+"unable to receive message")
                s.close()
                sys.exit() 
                
                
                
                                     
  #class to handle bot replies                      
class bot_replies():
    def _init_(self,server,channel):
        self.server=server
        self.channel=channel
        self.sock=s.socket(s.AF_INET, s.SOCK_STREAM)
    #function to handle random replies when in a channel
    def random_replies():
       randlist=["hello",
                    "how are you",
                    "whoaaa",
                    "I am a bot",
                    "hush",
                    "cold",
                    "i get you",
                    "i understand",
                    "will let you know",
                    
                 ]
       msg=rand.choice(randlist)
       print(msg)
       bot.send_message(channel,msg)
     
    
            
    def privatemsg(self,usr):
     self.sock.send(bytes ( "PRIVMSG "+usr+""+rand.choice(list(open("facts.txt")))+"\r\n", "UTF-8"))
    
       
if __name__=="__main__":
    server="127.0.0.1"
    channel="#Test"
    name="bot_peter"
    nickname="ruthlessbot"
    print("#"*50)
    bot=bot(server, channel, name, nickname)
    bot.main()
    
               
    
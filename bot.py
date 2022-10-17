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
         

    def main(self):
        user_list=[name]
        #while loop to handle connection, sending of messages and receiving of messages
        while True:
            
            
            #try receiving messages from server if failed print error and close socket
            try:
                data=self.sock.recv(1024).decode("UTF-8")
                
                print(user_list)
                print("*"*50)
                if data.find("PING")!=-1:
                    self.sock.send(bytes("PONG "+data.split()[1]+"\r\n", "UTF-8"))
                if data.find("PRIVMSG")!=-1:
                    message=data.split("PRIVMSG",1)[1].split(":",1)[1]
                    if message.startswith("!"):
                        if message.startswith("!hello"):
                            self.send_message(channel, "Hello")
                        elif message.startswith("!help"):
                            self.send_message(channel, "Commands: !hello, !help, !roll, !quit")
                        elif message.startswith("!roll"):
                            self.send_message(channel, str(rand.randint(1,6)))
                            
                        elif message.find("PRIVMSG"+self.name) != -1:
                          print("received a private message")
                          usr=message.split("!",1)[0][1:]
                          bot_replies.privatemsg(usr)  
                             
                        elif message.startswith("!quit"):
                            self.send_message(channel, "Bye")
                            self.sock.close()
                            sys.exit()
                        elif message.find("QUIT") != -1:
                            usr=message.split("!",1)[0][1:]
                            user_list.remove(usr)
                            print(f"{usr} has left the channel")
                            print(user_list)
                        elif message.find("JOIN") != -1:
                            usr=message.split("!",1)[0][1:]
                            user_list.append(usr)
                            print(f"{usr} has joined the channel")
                            print(user_list)    
                            
                        else:
                            self.send_message(channel, "Command not found")
            except s.error as e:
                print("Error: "+str(e)+"unable to receive message")
                s.close()
             
                
                
                
                                     
  #class to handle bot replies                      
class bot_replies():
    def _init_(self,server,channel):
        self.server=server
        self.channel=channel
        self.sock=s.socket(s.AF_INET, s.SOCK_STREAM)
    #function to handle random replies when in a channel
    def random_replies(self,msg,dest,user_list):
        if msg.find("!Hello")!=-1:
            self.send_message( f"Hello {dest}")
        elif msg.find("!Hi")!=-1:
            self.send_message( f"Hi {dest}")
        elif msg.find("!slap") !=-1:
            self.send_message( f"{dest} slaps {user_list[rand.randint(0,len(user_list))]}")
        
    
    #function to send random facts when private messaged
    def random_facts(self,filename,dest):
     if filename=="":
        print("Error: filename is empty")
        sys.exit(-4)
     else:
    #open file 
     
      with open(filename,"r") as file:
         #read lines
            facts=file.readline()
            # pick a random fact from the lines read 
            fact=rand.choice(facts)
            #send fact to user
            bot.send_message(channel, fact) 
            #print to console
            print(f"sent {fact} to {channel}")
            
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
    
               
    
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
        #while loop to handle connection, sending of messages and receiving of messages
        while True:
            data=self.sock.recv(1024)
            data=data.decode("UTF-8")
            data=data.strip('\n\r') 
            if("PRIVMSG" in data):
                Split_message=data.split(":")
                msg=Split_message[2]
                if(msg.__contains__("!")):
                 message=msg[1] 
                 message=message.split(" ")[0] 
                 commands.command_library(message)
                 if self.name in msg[1]:
                        print("message from "+msg[0]+" : "+msg[1])
                        
                        to_who=str(msg[1].split("!")[0])
                        random_facts(to_who,"facts.txt")
                else:
                    if data.find("PING") !=-1:
                     self.sock.send(bytes("PONG "+data.split()[1]+"\r\n", "UTF-8"))
                     print("pinged")
                        #if data contains PING send PONG to server and print pinged to console
                   
                        
  #class to handle bot replies                      
class bot_replies():
    def _init_(self,server,channel):
        self.server=server
        self.channel=channel
    #function to handle random replies when in a channel
    def random_replies(self):
        replies=["Hello", 
                 "Hi",
                 "How are you?",
                 "I am fine",
                 "interesting",
                 "whoaaaa",
                 "nice",
                 "decent"]
        reply=rand.choice(replies)
        
        bot.send_message(self.channel, reply)
        print(f"sent {reply} to {self.channel}")
    
    #function to send random facts when private messaged
def random_facts(self,filename):
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
            bot.send_message(self.channel, fact) 
            #print to console
            print(f"sent {fact} to {self.channel}")
              
       
    #main function         
if __name__=="__main__":
    server="127.0.0.1"
    channel="#Test"
    name="bot_peter"
    nickname="ruthlessbot"
    bot=bot(server, channel, name, nickname)
    print("#"*50)
    bot.main(server)           
    
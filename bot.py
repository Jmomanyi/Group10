#!/bin/python3


import socket as s#import socket library
import sys #imports sys library
import os #imports os library
import random as rand #imports random library

 
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
        self.user_list=[self.name]
        self.connect_to_server()
        self.join_channel(self.channel)
        #conect to server
    def connect_to_server(self):
        #try connecting to server and if it fails, print error and exit
        try:
            self.sock.connect((self.server, 6667))
            print(f"connected to {self.host_ip}")
            
            #identify itself
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
      
      #get the name of the user who messaged           
    def  get_user(self,data):
        user=data.split()
        user=user[0].strip(":!,@")
        return user
    
    #add the user to the list of users
    def add_user(self,user):
        self.user_list.append(user)
        return self.user_list
    
    #remve the user from list if the user leaves the channel
    def remove_user(self,user):
        if user not in self.user_list:
            print("User not in list")
        else:
            self.user_list.remove(user)
            return self.user_list

#get the uselist
    def get_user_list(self):
        self.sock.send(bytes("NAMES "+self.channel+"\r\n","UTF-8"))
        print(self.user_list)
        return self.user_list
    

       
    
    def main(self):
                    
                
        #while loop to handle connection, sending of messages and receiving of messages
        while True:
            
            
            #try receiving messages from server if failed print error and close socket
            try:
                data=self.sock.recv(1024).decode("UTF-8")
                #receives ping from the server and sends pong back to keep connection alive
                if data.find("PING")!=-1:
                    self.sock.send(bytes("PONG "+data.split()[1]+"\r\n", "UTF-8"))
                    
                    #
                    print("*"*20)
                    print("USERLIST")
                    
                    print(self.user_list)
                    
                    print("*"*20)



                #keep track of users in channel who JOIN
                if data.find("JOIN")!=-1:
                    user=self.get_user(data)
                    self.add_user(user)
                    print(user+" HAS JOINED CHANNEL.")
                    bot.get_user_list()

              #Keep track of u#Keep track of users in channel who PART
                elif data.find("QUIT")!=-1:
                    user=self.get_user(data)
                    bot.remove_user(user)
                    print("USER LEFT: "+user)
               
                elif   data.find("PRIVMSG"+self.name+":")!=-1:
                  print("I was mentioned")
                  recv=self.get_user(data)
                  bot_replies.privatemsg(self,recv)
                   
                
                        
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
                            who=self.get_user(data)
                            time=os.popen("date").read()
                            self.send_message(self.channel, "Hello "+who+". It is "+time)
                        elif message.startswith("!help"):
                            self.send_message(channel, "Commands: !hello, !help, !roll, !slap")
                        elif message.startswith("!roll"):
                            diceroll=rand.randint(1,6)
                            self.send_message(channel, f"You rolled a {diceroll}")
                        elif message.startswith("!slap"):
                            randuser=rand.choice(self.user_list)
                            if randuser==self.name:
                                self.send_message(channel, f"Can't slap myself")
                            else:     
                              self.send_message(channel,"slaps"+" "+randuser+" "+"with a large trout. \n")
                                   
                        
                        else:
                            self.send_message(channel, "Command not recognised")          
                                  
                    else:   
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



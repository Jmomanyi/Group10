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
        self.host_ip=s.gethostbyname(s.gethostname())#get the host ip
        self.user_list=[] #list of users in the channel
        self.connect_to_server()#call connect to server function
        self.join_channel(self.channel)#call join channel function
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
            #print error and exit
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
            try:#join channel
                self.sock.send(bytes("JOIN "+channel_name+"\r\n", "UTF-8"))
                #identify itself to the channel
                self.sock.send(bytes("PRIVMSG "+channel_name+" :Hello, I am a"+self.nickname+" !\r\n", "UTF-8"))
                print("joined channel "+channel_name)
            #print error and close socket
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
                #send message
                self.sock.send(bytes("PRIVMSG "+dest+" :"+message+"\r\n", "UTF-8"))
                #print error and close socket
            except s.error as e:
                print("Error: "+str(e)+"unable to send message")
                s.close()     
      
      #get the name of the user who messaged           
    def  get_user(self,data):
        msg=data.split('\n\r')#remove extra bits
        usr=msg[0].split(":")#split to obtain the name of the user
        us=usr[1]#the name of the user is in the seond index of the mssg received
        if (self.name in usr[1])!=-1:
            if usr[1] != "":#if the name is not empty
            #get the name of the user who messaged and convert to string
              whotosend=str(usr[1].split('!')[0])
              #return the name of the user
        return whotosend      
    
    #got this from this website
    #https://www.w3schools.com/python/trypython.asp?filename=demo_list_append
    #add the user to the list of users
    def add_user(self,user):
        self.user_list.append(user)
        return self.user_list
    
    #remve the user from list if the user leaves the channel
#https://note.nkmk.me/en/python-list-clear-pop-remove-del/#:~:text=In%20Python%2C%20use%20list%20methods,with%20an%20index%20or%20slice.
    def remove_user(self,user):
        if user not in self.user_list:
            print("User not in list")
        else:
            self.user_list.remove(user)
            return self.user_list

#get the uselist
    def get_user_list(self):
        for user in self.user_list:
           user_list=[self.name]
           user_list.append(user)
           print(user_list)
    

       
    #https://realpython.com/python-sockets/
    def main(self):
                    
                
        #while loop to handle connection, sending of messages and receiving of messages
        while True:
            
            
            #try receiving messages from server if failed print error and close socket
            try:
                data=self.sock.recv(1024).decode("UTF-8")
                if not data:
                    print("Server OUT")
                    break
                #receives ping from the server and sends pong back to keep connection alive
                if data.find("PING")!=-1:
                    self.sock.send(bytes("PONG "+data.split()[1]+"\r\n", "UTF-8"))
                    
                    #print user list
                    print("*"*20)
                    print("USERLIST")
                    bot.get_user_list()  
                    print("*"*20)



                #keep track of users in channel who JOIN
                if data.find("JOIN")!=-1:
                    user=self.get_user(data)
                    self.add_user(user)
                    print(user+" HAS JOINED CHANNEL.")
                    
                    #print user list
                    print("*"*20)
                    print("USERLIST")
                    bot.get_user_list()
                    print("*"*20)

              #Keep track of u#Keep track of users in channel who PART
                elif data.find("QUIT")!=-1:
                    user=self.get_user(data)
                    bot.remove_user(user)
                    print("USER LEFT: "+user)
                    
                    #print updated userlist
                    print("*"*20)
                    print("USERLIST")
                    bot.get_user_list()
                    print("*"*20)
                
                
                        
               #respond to messages in channel
                #respond hello
                #provide help
                #roll a dice
                #slap a user
                if data.find("PRIVMSG")!=-1:
                    whotosend=self.get_user(data)    
                    messagetosend=rand.choice(list(open("facts.txt")))
                    print(whotosend)
                    self.send_message(whotosend,messagetosend)
                    
                     #else try sending message if failed print error and close socket     
                 
                    message=data.split("PRIVMSG",1)[1].split(":",1)[1]
                    print(message)
                    #if message starts with !
                    if message.startswith("!"):
                        #if a message starts with hello
                        if message.startswith("!hello"):
                            who=self.get_user(data)#get the name of the user who messaged
                            time=os.popen("date").read()#get the time
                            
                            #if a message starts with help
                        elif message.startswith("!help"):
                            #send list of commands
                            self.send_message(channel, "Commands: !hello, !help, !roll, !slap")
                            #if a message starts with roll
                        elif message.startswith("!roll"):
                            #choose a random number between 1 and 6
                            diceroll=rand.randint(1,6)
                            #send the random number
                            self.send_message(channel, f"You rolled a {diceroll}")
                            #if a message starts with slap
                        elif message.startswith("!slap"):
                            #get a random user from the list of users in the channel
                            randuser=rand.choice(self.user_list)
                            #while the random user is the bot
                            while randuser==self.name:
                                #get another random user
                                randuser=rand.choice(self.user_list)
                                #else
                            else:     
                               #slap a random user with a trout
                              self.send_message(channel,"slaps"+" "+randuser+" "+"with a large trout. \n")
                               
                               
                                  
                        else:   
                            #reply random replies
                          bot_replies.random_replies()
              #              
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
    #function to handle random replies when its not a command
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
       msg=rand.choice(randlist)#get a random message from the list
       #send the message to the channel
       bot.send_message(channel,msg)
     

       
    
#main function       
if __name__=="__main__":
 
    server="127.0.0.1"
    channel="#BOTS"
    name="bot_peter"
    nickname="ruthlessbot"
    
    print("#"*50)
    bot=bot(server, channel, name, nickname)

    bot.main()



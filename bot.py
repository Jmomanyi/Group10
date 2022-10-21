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
        #gets the host ip
        self.host_ip=s.gethostbyname(s.gethostname())
        #list of users in the channel
        self.user_list=[self.name] 
        #call connect to server function
        self.connect_to_server()
        #call join channel function
        self.join_channel(self.channel)

    #conect to server
    def connect_to_server(self):
        #try connecting to server and if it fails, print error and exit
        try:
            self.sock.connect((self.server, 6667))
            print(f"Connected to {self.host_ip}")
            
            #sends nick name.
            self.sock.send(bytes("USER "+self.nickname+" "+self.nickname+" "+self.nickname+" :"+self.nickname+"\r\n", "UTF-8"))
            self.sock.send(bytes("NICK "+self.name+"\r\n", "UTF-8"))
        except s.error as e:
            #print error and exit
            print(f"Error: {str(e)} Unable to connect to server.")
            sys.exit()
            
    #join channel function.
    def join_channel(self, channel_name):
        #if channel is empty print to console channel empty and exit
        if channel_name=="":
            print("Error: Channel name is empty.")
            sys.exit(-1)
            
            #else try joining channel if failed print error and close socket
        else:
            try:#join channel
                self.sock.send(bytes("JOIN "+channel_name+"\r\n", "UTF-8"))
                #bot identifies itself.
                self.sock.send(bytes("PRIVMSG "+channel_name+" :Hello, I am a"+self.nickname+" !\r\n", "UTF-8"))
                print("Joined channel "+channel_name)
            #print error and close socket if failed
            except s.error as e:
                print("Error: "+str(e)+"Unable to join channel.")
                s.close()
                
      
    #send message function
    def send_message(self,dest, message):
        #if destination is empty print error and exit
        if dest=="":
            print("Error: Destination is empty.")
            sys.exit(-2)
            #if message is empty print error and exit
        if message=="":
                print("Error: Message is empty.")
                sys.exit(-3)
        #else try sending message if failed print error and close socket
        else:
            try:
                #send message
                self.sock.send(bytes("PRIVMSG "+dest+" :"+message+"\r\n", "UTF-8"))
                #print error and close socket
            except s.error as e:
                print("Error: "+str(e)+"Unable to send message.")
                s.close()     

      
    #gets name of the user who sent the message           
    def  get_user(self,data):
        #remove extra bits
        msg=data.split('\n\r')
        #split to obtain the name of the user
        usr=msg[0].split(":")
        #the name of the user is in the second index of the message received
        us=usr[1] 
        if (self.name in usr[1])!=-1:
                #if the name is not empty
                if usr[1] != "":
                    try:
                        #get the name of the user who messaged and convert to string
                        whotosend=str(usr[1].split('!')[0])
                    except s.error as e:
                        print("Error: "+str(e)+"Unable to get user.")
                        s.close()
        #return the name of the user
        return whotosend 


    
    
    #adds user to the list of users
    def add_user(self,user):
        #got this from this website
        #https://www.w3schools.com/python/trypython.asp?filename=demo_list_append
        self.user_list.append(user)
        #return self.user_list
        return self.user_list

    
    #removes user from list if the user leaves the channel
    def remove_user(self,user):
        #if user is not in the list
        if user not in self.user_list:
            #prints user not in list
            print("User not in list")
        #else remove user from list   
        else:
            #https://note.nkmk.me/en/python-list-clear-pop-remove-del/#:~:text=In%20Python%2C%20use%20list%20methods,with%20an%20index%20or%20slice.
            self.user_list.remove(user)
            return self.user_list

    def get_content(self,data):
        msg=data.split('\n\r')
        mess=msg[2].split(":")
        
    #gets the user_list and prints it
    def get_user_list(self):
        for user in self.user_list:
            #got this from this website
            #https://www.w3schools.com/python/trypython.asp?filename=demo_list_append
           user_list=[]
           user_list.append(user)
           print(user_list)
    

       
    #https://realpython.com/python-sockets/
    def main(self):
                    
                
        #while loop to handle connection, sending of messages and receiving of messages
        while True:
            
            
            #try receiving messages from server if failed print server out and exit.
            try:
                data=self.sock.recv(1024).decode("UTF-8")
                if not data:
                    print("Server Out.")
                    break

                #receives ping from the server and sends pong back to keep connection alive
                if data.find("PING")!=-1:
                    self.sock.send(bytes("PONG "+data.split()[1]+"\r\n", "UTF-8"))
                    
                    #prints the user list
                    print("*"*20)
                    print("USERLIST.")
                    bot.get_user_list()  
                    print("*"*20)



                #keeps track of users who JOIN channel
                if data.find("JOIN")!=-1:
                    #gets the name of the user who joined
                    user=self.get_user(data)
                    #adds user to the list
                    self.add_user(user)
                    print(user+" HAS JOINED CHANNEL.")
                    
                    #print updated userlist
                    print("*"*20)
                    print("USERLIST.")
                    bot.get_user_list()
                    print("*"*20)


                #Keeps track of users who leave channel
                elif data.find("QUIT")!=-1:
                    #gets the name of the user who left
                    user=self.get_user(data)
                    #removes user from the list
                    bot.remove_user(user)
                    print("USER LEFT: "+user)
                    
                    #print updated userlist
                    print("*"*20)
                    print("USERLIST.")
                    bot.get_user_list()
                    print("*"*20)
                
                
                        
                     #respond to messages in channel
                    #respond hello
                    #provide help
                    #roll a dice
                    #slap a user
                
                    
                    #split data to get the message sent and print it
                    message=bot.get_content(data)
                    print(message)

                    #if message starts with !
                    if message.startswith("!"):
                        #if a message starts with hello
                        if message.startswith("!hello"):
                            #get the name of the user who messaged
                            who=self.get_user(data)
                            #get the time of the day
                            time=os.popen("date").read()
                            
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
                            
                if data.find("PRIVMSG")!=-1:
                    #gets name of user to send message to
                    whotosend=self.get_user(data)  
                    #gets the message to send  
                    messagetosend=rand.choice(list(open("facts.txt")))
                    print(whotosend)
                    #sends message to user
                    self.send_message(whotosend,messagetosend)
                                    
                            
            #if failed, print error and exit.            
            except s.error as e:
                print("Error: "+str(e)+"Unable to receive message.")
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
        #list of random replies
       randlist=["Hello.",
                    "How are you?",
                    "Whoaaa!",
                    "I am a bot.",
                    "Hush!",
                    "Cold.",
                    "I get you.",
                    "I understand.",
                    "Will let you know.",]
        #get a random message from the list
       msg=rand.choice(randlist)
       #send the message to the channel
       bot.send_message(channel,msg)
     

       
    
      
if __name__=="__main__":
    
    #assigns the server,channel, name and nickname to variables
    server="127.0.0.1"
    channel="#BOTS"
    name="bot_peter"
    nickname="ruthlessbot"
    print("#"*50)
    #create an instance of the bot class and pass the server, channel, name and nickname as arguments.
    bot=bot(server, channel, name, nickname)
    #call the main function
    bot.main()



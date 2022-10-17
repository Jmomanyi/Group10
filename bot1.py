import Bot_commands as commands
import socket as s
import sys
import os
import random as rand

class bot():
    def __init__(self,server,channel,name,nickname):
        self.server=server
        self.channel=channel
        self.name=name
        self.nickname=nickname
        self.sock=s.socket(s.AF_INET, s.SOCK_STREAM)
        self.host_ip=s.gethostbyname(s.gethostname())
        self.user_list=[]
        self.connect_to_server()
        self.join_channel(self.channel)
        
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
        
    def join_channel(self,channelname):
        #if channel is empty print to console channel empty and exit
        if channelname=="":
            print("Error: channel name is empty")
            sys.exit(-1)
            
            #else try joining channel if failed print error and close socket
        else:
            try:
                self.sock.send(bytes("JOIN "+channelname+"\r\n", "UTF-8"))
                print("joined channel "+channelname)
                self.sock.send(bytes("PRIVMSG "+channelname+" :Hello, I am a"+self.nickname+" !\r\n", "UTF-8"))
            except s.error as e:
                print("Error: "+str(e)+"unable to join channel")
                s.close()
        
    def message_handler(self,):
        self.user_list=[name]
        data=self.sock.recv(1024).decode("UTF-8")
        print("LIST OF USERS ")
        print(data)
        print("*"*50)
        if data.find("PING")!=-1:
          self.sock.send(bytes("PONG "+data.split()[1]+"\r\n", "UTF-8"))
          
        if data.find("PRIVMSG")!=-1:
          message=data.split()
          source =message[0].strip(":")
          content=' '.join(message[3:]).strip(":")
        #https://www.w3schools.com/python/trypython.asp?filename=demo_list_append
          self.user_list.append(source)
          print(self.userlist)
          print(f"source: {source} content: {content}")
          bot_replies.privatemsg(source)
          
        if content.find("!help")!=-1:
            commands.commands.help()
            
                            
                        
            
                
            
            
class bot_replies():
    def __init__(self,server,channel,name,nickname):
     self.server=server
     self.channel=channel
     self.name=name
     self.nickname=nickname
     self.socket=s.socket(s.AF_INET, s.SOCK_STREAM)
    def privatemsg(self,usr):
         self.socket.send(bytes ( "PRIVMSG "+usr+""+rand.choice(list(open("facts.txt")))+"\r\n", "UTF-8"))
        
    def send_message(self,message):
        self.socket.send(bytes("PRIVMSG "+self.channel+" :"+message+"rn", "UTF-8"))  
        
          
            
class channels():    
    def __init__(self,channel):
        self.channel=channel
        self.user_list=[]
        
        
    def add_user(self,usr): 
        self.user_list=[name]
        self.user_list.append(usr)
        print(f"{usr} joined")
        print(self.user_list)
        
    def remove_user(self, usr):       
        if usr not in self.user_list:
            self.user_list.remove(usr)
            print("user quit")
if __name__=="__main__":
 server="127.0.0.1"
 channel="#Test"
 name="bot_peter"
 nickname="ruthlessbot"
 
 while True:
   print("#"*50)
   bot=bot(server,channel,name,nickname)
   bot.message_handler()
 
 
 
 
 



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
        
        data=self.sock.recv(1024).decode("UTF-8")
        print("LIST OF USERS ")
        print(data)
        print("*"*50)
        if data.find("PING")!=-1:
          self.sock.send(bytes("PONG "+data.split()[1]+"\r\n", "UTF-8"))
        if data.find("PRIVMSG")!=-1:
          message=data.split("PRIVMSG",1)[1].split(":",1)[1]
      
        if message.startswith("!help"):
              commands.commands.help()
            
                            
                        
            
                
            
            
class bot_replies():
    def __init__(self,server,channel,name,nickname):
     self.server=server
     self.channel=channel
     self.name=name
     self.nickname=nickname
    def private_message(self,username,message):
        self.sock.send(bytes("PRIVMSG "+username+" :"+message+"rn", "UTF-8"))
        
    def send_message(self,message):
        self.sock.send(bytes("PRIVMSG "+self.channel+" :"+message+"rn", "UTF-8"))    
            
class channels():    
    def __init__(self,channel):
        self.channel=channel
        self.user_list=[]
        
        
    def add_user(self,usr): 
        user_list=[name]
        user_list(list(set(usr)))
    def remove_user(self, usr):       
        if usr in self.user_list:
            self.user_list.remove(usr)
            print(self.user_list)
if __name__=="__main__":
 server="127.0.0.1"
 channel="#Test"
 name="bot_peter"
 nickname="ruthlessbot"
 print("#"*50)
 bot=bot(server,channel,name,nickname)
 while True:
  bot.message_handler
 
 
 
 
 



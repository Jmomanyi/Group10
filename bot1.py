
import socket as s #import socket
import sys #import sys
#import random 
import random as rand
import time
#class bot 

class bot():
    #receive server channel name and nickname as parameters to construct class
    def __init__(self,server,channel,name,nickname):
        self.server=server
        self.channel=channel
        self.name=name
        self.nickname=nickname
        self.sock=s.socket(s.AF_INET, s.SOCK_STREAM)
        self.host_ip=s.gethostbyname(s.gethostname())
        self.user_list=[self.name]
        self.connect_to_server()#call connnect to server method
        self.join_channel(self.channel)#call the join channel method
        
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
    def  get_user(self,data):
        user=data.split()
        user=user[0].strip(":!,@")
        return user
    def message_handler(self,):
        #the bot is the only one in the channel at start
        
        #read messages from server and decode
        data=self.sock.recv(1024).decode("UTF-8")
       
        #if the message is a ping, reply with pong to keep connection alive
        if data.find("PING")!=-1:
          self.sock.send(bytes("PONG "+data.split()[1]+"\r\n", "UTF-8"))
          
        if self.name in data:
          source=bot.get_user(data)
          print(f"source: {source} content: {data}")
          msg=rand.choice(list(open("facts.txt")))
          print(msg)
          self.sock.send(bytes("PRIVMSG "+source+" :"+msg+"\r\n", "UTF-8"))
          
         
        
            
                            
                        
            
                
            
            
class bot_replies():
    def __init__(self,server,channel,name,nickname):
     self.server=server
     self.channel=channel
     self.name=name
     self.nickname=nickname
     self.socket=s.socket(s.AF_INET, s.SOCK_STREAM)
    
        
    def send_message(self,channel,message):
        #if destination and message are empty print error 
        if channel!="" and message!="":
           
            self.socket.send(bytes("PRIVMSG "+channel+" :"+message+"\r\n", "UTF-8"))
        else:
            print("Error: channel or message is empty")
          

if __name__=="__main__":
 server="127.0.0.1"
 channel="#Test"
 name="bot_peter"
 nickname="ruthlessbot"
 bot=bot(server,channel,name,nickname)
 while True:
  
   
   bot.message_handler()
 
 
 
 
 



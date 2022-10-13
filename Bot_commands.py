#!/bin/python3
import bot as Bot
import socket as s


#class to handle bot commands
class commands():
   
    def command_library(command):
       
        if command=="!Help":
            Bot.send_message(f"hello, I am {Bot.nickname} !"
                             +"i can take the following commands:"
                             +"!Help"
                             +"!Hello"
                             +"slap")
        if command=="!Hello":
            Bot.send_message("hello")    
        if command=="!Slap":
            Bot.send_message("slap")
        else:
            Bot.send_message("I don't know this command")  
           
    
      
  
    
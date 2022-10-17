#!/bin/python3
import bot as Bot
import socket as s
import bot1 as Bot1


#class to handle bot commands
class commands():
   
    def help():
        Bot1.bot_replies.send_message("Hello I am a bot"
              +"i can take the following commands "+
              "___________________________________"+
              "1. !help - displays this message"+
              "2. !roll - rolls a dice"+
              "3. !flip - flips a coin"+
              "4.!slap - slaps a user")
           
    
      
  
    
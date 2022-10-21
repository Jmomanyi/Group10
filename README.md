Internet Relay Chat(IRC) server with a few basic functions

Description:

An internet relay Server written in python that uses sockets to connect to an irc client capable of implementing basic IRC protocols and commands,
it listens for an IPv6 connects from any address and on the port 6667


Features:
•	It allows clients to connect using a nickname and username of their choice
•	It also allows the user to send a private message to another user 
•	It allows clients to join or create a channel and also communicate to other users in the channel
•	it allows a user to leave the channel
•	it allows a user to quit the server
•	it allows an admin to kick any one out of the channel
•	it handles error perfectly except kepboard interrupt error
•	it allows the users to list out the names of all the users in the same channels
•	it conforms IRC protocols and command
•	it also handles the connection of multiple clients to the server



Limitations:
     # quiting the server needs you to press ctrl+c twice
     
 
 # a bot is used as the client and the server the host 
 # to see what the bot can do use hexchat
 # to launch hexchat use ip as >::1/6667<

BOT.PY
To launch the bot on terminal
 >python3 bot.py<
 # remember the bot will only work if miniircd server is already running locally

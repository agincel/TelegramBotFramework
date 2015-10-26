import csv
import re
import traceback
import time

import telegram

import src.botCommands as botCommands

APIKEY = ''

#open Telegram and start a chat with BotFather, to create a new bot
#you'll receive a token, replace the dummy token in apikey.csv with that

with open('apikey.csv', 'r+') as csvfile:
    reader = csv.DictReader(csvfile)
    APIKEY = list(reader)[0]['key']

bot = telegram.Bot(token=APIKEY)

updates = {}
currentMessage = {}

print "Telegram Bot Welcome Message"
print "Framework by Adam Gincel"

newestOffset = 0
networkFailure = True
while networkFailure: #pings until connection is established
    try:
        updates = bot.getUpdates(offset=newestOffset)
        for u in updates:
            newestOffset = u.update_id
        networkFailure = False
    except Exception:
        print traceback.format_exc()
        print "...",
print "...Connected!"

instanceAge = 0 #age in seconds
refreshRate = 2.5 #seconds in between each refresh
chat_id = 0

running = True
while running:
    networkFailure = True
    while networkFailure:
        try:
            updates = bot.getUpdates(offset=newestOffset+1)
            for u in updates:
                newestOffset = u.update_id
            networkFailure = False
        except Exception:
            print "...",

    if instanceAge % (refreshRate * 10) == 0: #print 1 Y every eight ticks
        print "Y"
    else:
        print "X",


    for u in updates: #iterate through all messages received
        currentMessage = u.message
        try:
            chat_id = currentMessage.chat.id
            parsedCommand = re.split(r'[@\s:,\'*]', currentMessage.text.lower())[0] #get first word (ie: /hello)

            running = botCommands.process(bot, chat_id, parsedCommand, currentMessage.text, currentMessage, u, instanceAge)
            #This sends a lot of info to the process method, which handles individual methods. A breakdown:

            #bot: the bot instantiated here with your APIKEY. Used later on to send messages.
            #chat_id: the ID of the chat from the message; this is where the messages get sent
            #parsedCommand: used to check what command is being used; if /hello aiwbgawyegai is entered, parsedCommand is /hello
            #currentMessage.text: the method calls this messageText; the entire sent text (ie /hello aiwbgawyegai)
            #currentMessage: the telegram struct Message, which has info about who sent it, the time it was sent, etc
            #u, the update, which has a bit more info than the message. Rarely used.
            #instanceAge: a thing I made up. An int showing how many seconds this instance of the bot has been running.

        except Exception as myException:
            print traceback.format_exc()

    instanceAge += refreshRate
    time.sleep(refreshRate)

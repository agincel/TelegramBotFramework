import csv
import re
import traceback
import os

import telegram
import botSendFunctions

chatInstanceArray = {}
messageSent = 1

#Short tutorial:

#To send a text message, use the method sendText("text")
#To make the message a reply to another message: use sendText("text", replyingMessageID=(the id of the message to reply to))
#To create a custom keyboard with your message: use sendText("text", keyboardLayout)

#to send an image just call sendPhoto("imagename.filetype")

#to make a command less spammable, put this line before the command's contents:
#if passSpamCheck():



def process(bot, chat_id, parsedCommand, messageText, currentMessage, update, instanceAge):
    global messageSent

    def sendText(givenText, replyingMessageID=0, keyboardLayout=[]):
        global messageSent
        messageSent += 1
        botSendFunctions.sendText(bot, chat_id, givenText, replyingMessageID, keyboardLayout)

    def sendPhoto(imageName): #looks for images in the /images folder
        global messageSent
        messageSent += 1
        botSendFunctions.sendPhoto(bot, chat_id, "images/"+ imageName)

    def passSpamCheck():
        return botSendFunctions.spamCheck(chat_id, currentMessage.date)
        #this is tracked the same for all commands; if two commands are marked
        #with this, and one is used, the other one will not work for 15 seconds
        #as well. This is for ease of programming. Feel free to modify if you want

    try:
        try:
            chatInstanceArray[chat_id]['checking'] = True
        except Exception:
            chatInstanceArray[chat_id] = {'checking': True} #place any information you want to keep track of during this instance here, it is indexed by chat_id


        #COMMANDS GO HERE
        #
        #parsedCommand is set to lowercase, so only check for lowercase commands
        #

        if parsedCommand == "/ping":
            sendText("pong")

        elif parsedCommand == "/image":
            sendPhoto("testimage.png")

        elif parsedCommand == "/replytome":
            sendText("I\'m replying to you.", replyingMessageID=currentMessage.message_id)

        elif parsedCommand == "/customkeyboard":
            sendText("Here\'s a keyboard:", keyboardLayout=[["/killKeyboard", "/killKeyboard"], ["/killKeyboard", "/killKeyboard"]])

        elif parsedCommand == "/killkeyboard":
            sendText("This is configured to kill a keyboard when any message is received, this can be changed in SendFunctions.")

        elif parsedCommand == "/unspammable":
            if passSpamCheck():
                sendText("NO SPAMMING")


        #This is the help function. I'd recommend telling BotFather to add this command to the commandlist.
        elif parsedCommand == "/help":
            response = "/ping - returns pong\n"
            response += "/image - sends a test image\n"
            response += "/replytome - sends a reply\n"
            response += "/customkeyboard - sends a custom keyboard\n"
            response += "/killkeyboard - removes a custom keyboard\n"
            response += "/unspammable - cannot use more than once per 15 seconds\n"
            response += "add more commands here"

            sendText(response)

        return True

    except Exception:
        print traceback.format_exc()
        return True

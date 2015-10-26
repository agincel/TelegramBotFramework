import csv
import re
import traceback
import os
import time

import telegram

spamLimitTime = 15

spamArray = {}

def spamCheck(chat_id, date):
    global spamArray
    global spamLimitTime
    try:
        spamArray[chat_id]['checking'] = True
    except Exception:
        spamArray[chat_id] = {'checking': True, 'spamTimestamp': 0}

    if time.mktime(date.timetuple()) - spamLimitTime > spamArray[chat_id]['spamTimestamp']:
        spamArray[chat_id]['spamTimestamp'] = time.mktime(date.timetuple())
        return True
    else:
        return False


def sendText(bot, chat_id, messageText, replyingMessageID=0, keyboardLayout=[], killkeyboard=True):
    bot.sendChatAction(chat_id=chat_id, action='typing')
    try:
        print messageText + " at " + str(chat_id)
    except Exception:
        print "Sent something with weird characters to " + str(chat_id)

    if replyingMessageID != 0:
        bot.sendMessage(chat_id=chat_id, text=messageText, reply_to_message_id=replyingMessageID, reply_markup=telegram.ReplyKeyboardHide(hide_keyboard=killkeyboard))
    elif keyboardLayout != []:
        print "Sending keyboard at " + str(chat_id)
        bot.sendMessage(chat_id=chat_id, text=messageText, reply_markup=telegram.ReplyKeyboardMarkup(keyboard=keyboardLayout, one_time_keyboard=True, resize_keyboard=True))
    else:
        bot.sendMessage(chat_id=chat_id, text=messageText, reply_markup=telegram.ReplyKeyboardHide(hide_keyboard=killkeyboard))

def sendPhoto(bot, chat_id, imagePath):
    bot.sendChatAction(chat_id=chat_id, action='upload_photo')
    print "Sending picture to " + str(chat_id)
    bot.sendPhoto(chat_id=chat_id, photo=open(imagePath, "rb"))

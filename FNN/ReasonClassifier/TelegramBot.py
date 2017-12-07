import telepot
import time
import nltk
from nltk.stem.lancaster import LancasterStemmer
import os
import json
import datetime

stemmer = LancasterStemmer()
import numpy as np
from lib import mods as m

time.sleep(1)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    chat_id = msg['chat']['id']
    command = msg['text']

    if command == '/start':
        newData = bot.sendMessage(chat_id, 'Hello! \nImagine that I am a Artificial Intelligence of the Smart House.' + \
                                  ' And you asked me to turn on or off a kettle, a lamp or an air conditioning, but I said that ' + \
                                  'other user with the same privileges said a conflicting order. As a result, I asked you to ' + \
                                  'say me why you want me to do your request. There are 6 classes of orders: health, security' + \
                                  ', energy, food, work and entertainment. Say somehow your reason in borders of these classes ' + \
                                  'and I will try to classify it. For example, you said "It is enough light from window" and I' + \
                                  ' classified it as "energy". If I guess correct, please, type +, else, please, type number of the' + \
                                  ' class. Numbers of the classes: 1 - health, 2 - security, 3 - energy, 4 - food, 5 - work, 6 - entertainment. \n Have a fun!')
    elif command == '+':
        newData = bot.sendMessage(chat_id, 'Thnx!')
    elif command == "1" or command == "2" or command == "3" or command == "4" or command == "5" or command == "6":
        newData = bot.sendMessage(chat_id, 'Confirmed!')
        with open('logTelega.txt', 'a') as the_file:
            stack = ['health', 'security', 'energy', 'food', 'work', 'entertainment']
            database = ": " + str(stack[(int(command) - 1)])
            the_file.write(database)
    else:
        type = m.classify(command)
        try:
            newData = bot.sendMessage(chat_id, type[0][0])
        except IndexError:
            newData = bot.sendMessage(chat_id, "I can`t classify")
        with open('logTelega.txt', 'a') as the_file:
            database = "\n" + str(command) + ": " + str(type) + " : " + str(newData[u'chat'])
            the_file.write(database)


bot = telepot.Bot('495414889:AAHrneNFrfGNWzrbfXakK-ib3Mn4LII_esA')
bot.message_loop(handle)

while 1:
    time.sleep(10)

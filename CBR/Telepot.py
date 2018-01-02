import telepot
from telepot.loop import MessageLoop
import time
import random
import datetime

token = '425620979:AAHfCI5dbvQLhWaOi-u0w3PmBQWg9hyG_cs'
bot = telepot.Bot(token)


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']

    if command == '/gm':
        file = "./kings.txt"
        with open(file, 'r') as f:
            lines = f.readlines()
            text = lines[-6:]
        texty = "The last lines of the kings.txt are: \n"
        for el in text:
            texty = texty + str(el)
        bot.sendMessage(chat_id, texty)
        bot.sendDocument(chat_id, open("./kings.txt", 'rb'))


MessageLoop(bot, handle).run_as_thread()

print("I am working...")
while 1:
    time.sleep(10)

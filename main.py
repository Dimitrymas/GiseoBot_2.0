import time

from sweater import bot
from sweater.chat_controller import listen_all

if __name__== '__main__':
    while True:
        try:
            bot.polling(non_stop=True, interval=0)
            listen_all
        except Exception as e:
            print(e)
            time.sleep(5)
            continue




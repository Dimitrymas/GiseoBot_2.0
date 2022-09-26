from sweater import bot
from sweater.chat_controller import listen_all

from telebot import apihelper

apihelper.proxy = {'https': 'https://user-uuid-96848eb9df224f4dba7b480365573ef5:465f91945752@zagent98.hola.org:22222'}




def start():
    try:
        listen_all
        bot.polling()
    finally:
        pass
if __name__ == '__main__':
    try:
        start()
    finally:
        pass

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

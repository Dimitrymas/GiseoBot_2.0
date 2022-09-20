from sweater import bot
from sweater.chat_controller import listen_all



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

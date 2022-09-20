from sweater.chat_controller.send_messages import *
from middlewares.user import MiddleUser
from sweater.controller.user_controller import UserController


def listen_commands(message):

    if message.text == "/start":
        UserController.start(message)

    elif message.text == "/menu":
        SendMessages.send_menu(message)

    elif message.text == "/diary":
        UserController.get_diary(message)






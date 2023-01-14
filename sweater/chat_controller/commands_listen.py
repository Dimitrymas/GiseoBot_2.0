from sweater.chat_controller.send_messages import *
from sweater.controller.user_controller import UserController


def listen_commands(message):
    if message.text == "/start":
        UserController.start(message)

    elif message.text == "/menu":
        SendMessages.send(message.chat.id, "Загрузка дневника, немного подождите")
        SendMessages.send_menu(message.chat.id)

    elif message.text == "/diary":
        UserController.get_diary(message)

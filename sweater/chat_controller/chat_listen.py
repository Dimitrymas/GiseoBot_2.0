from middlewares.user import MiddleUser
from sweater.chat_controller.send_messages import SendMessages
from sweater.controller.user_controller import UserController
from middlewares.time_convert import WeekTools as wt
from models.model import User

def listen_text(message):
    if message.text == "Дневник":
        SendMessages.send(message.chat.id, "Загрузка дневника, немного подождите")
        UserController.get_diary(message)
    elif message.text == "Долги":
        SendMessages.send(message.chat.id, "Загрузка пропущенных заданий")
        UserController.get_pastmandory(message)

    elif message.text == "Регистрация":
        UserController.registration_step_start(message=message)
    elif wt.is_day_button(message.text):
        UserController.get_day(message)
    elif wt.is_lesson_button(message.text):
        UserController.get_lesson(message)
    elif message.text == "Выбор дня":
        UserController.get_diary(message)
    elif message.text == "Следующая неделя":
        im_user = MiddleUser.get_user_by_chat(message.chat.id)
        im_user.set_week("plus")
        UserController.get_diary(message)
    elif message.text == "Текущая неделя":
        im_user = MiddleUser.get_user_by_chat(message.chat.id)
        im_user.set_week("that")
        UserController.get_diary(message)
    elif message.text == "Предыдущая неделя":
        im_user = MiddleUser.get_user_by_chat(message.chat.id)
        im_user.set_week("minus")
        UserController.get_diary(message)
    elif message.text == "Меню":
        SendMessages.send_menu(message.chat.id)




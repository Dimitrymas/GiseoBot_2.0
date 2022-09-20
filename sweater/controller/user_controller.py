from datetime import datetime, date

from telebot import types

from middlewares.user import MiddleUser
from middlewares.time_convert import WeekTools as wt
from models.model import City, User, School
from sweater import bot, session
from sweater.chat_controller.send_messages import SendMessages



class UserController:
    def registration_step_4(message):
        SendMessages.send(message.chat.id, "Отлично, вы зарегестрированны")
        Im_user = MiddleUser.get_user_by_chat(message.chat.id)
        Im_user.update(g_password=message.text)
        SendMessages.send_menu(message.chat.id)


    def registration_step_3(message):
        SendMessages.send(message.chat.id, "Отлично теперь введите пароль")
        Im_user = MiddleUser.get_user_by_chat(message.chat.id)
        Im_user.update(g_name=message.text)
        bot.register_next_step_handler(message, UserController.registration_step_4)

    def registration_step_2(message):
        school = School.query.filter(School.name == message.text).first()
        print(school)
        if school is None:
            SendMessages.send(message.chat.id, "Некорректная комманда")
        else:
            Im_user = MiddleUser.get_user_by_chat(message.chat.id)
            Im_user.update(school_id=school.id)
            SendMessages.send(message.chat.id, "Отлично, теперь введите логин от giseo")
            bot.register_next_step_handler(message, UserController.registration_step_3)

    def registration_step_1(message):
        buttons = types.ReplyKeyboardMarkup()
        name_city = message.text
        if City.query.filter(City.name==name_city).first() == None:
            SendMessages.send(message.chat.id, "Некорректная комманда")
        else:
            city = City.query.filter(City.name==name_city).first()
            schools = School.query.filter(School.city_id==city.id).all()
            for school in schools:
                buttons.add(types.KeyboardButton(f"{school.name}"))
            SendMessages.send(message.chat.id, "Выберите школу", buttons)
            bot.register_next_step_handler(message, UserController.registration_step_2)


    def registration_step_start(message):
        buttons = types.ReplyKeyboardMarkup()
        for city in City.query.all():
            buttons.add(types.KeyboardButton(f"{city.name}"))
        SendMessages.send(message.chat.id, "Ты начал регистрацию.\nВыбери свой город", buttons)
        bot.register_next_step_handler(message, UserController.registration_step_1)

    def start(message):
        MiddleUser.create_user(message.chat.id)
        SendMessages.send_start_message(message.chat.id)

    def get_diary(message):
        im_user = MiddleUser.get_user_by_chat(message.chat.id)
        diary = im_user.get_diary()
        print(diary)
        SendMessages.send_diary_week(message.chat.id, diary)

    def get_diary_back(message):
        im_user = MiddleUser.get_user_by_chat(message.chat.id)
        diary = im_user.get_json_week()
        SendMessages.send_diary_week(message.chat.id, diary)

    def get_day(message):
        SendMessages.send_diary_day(message.chat.id, wt.daydate_to_datestr(message.text))

    def get_lesson(message):
        SendMessages.send_diary_lesson(message.chat.id, message.text)



import telebot
from telebot import types

from middlewares.user import MiddleUser
from models.model import User
from sweater import bot
from sweater.controller.dairy_contraller import DairyController


class SendButtons:
    def drow_start_button():
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text="Регистрация", callback_data="registration")
        markup.add(button1)
        return markup


    def drow_menu_buttons(chat_id):
        buttons = types.ReplyKeyboardMarkup()
        Im_user = MiddleUser.get_user_by_chat(chat_id)
        print(chat_id)
        if Im_user.g_password != None:
            buttons.add(types.KeyboardButton("Дневник"))
        else:
            buttons.add(types.KeyboardButton("Регистрация"))
        return buttons


class SendMessages:
    def send_start_message(chat_id):

        commands = [telebot.types.BotCommand("/start", "Перезапуск бота или смена данных учетной записи"),
                    telebot.types.BotCommand("/menu", "Меню"), telebot.types.BotCommand("/diary", "Дневник")]
        print("send_start_message")
        bot.set_my_commands(commands)
        buttons = SendButtons.drow_start_button()
        bot.send_message(chat_id, "Привет я бот, у которого ты можешь узнать о своих оценках", reply_markup=buttons)

    def send_menu(message):
        print("send_menu")
        try:
            buttons = SendButtons.drow_menu_buttons(message.chat.id)
            bot.send_message(message.chat.id, "Меню:", reply_markup=buttons)
        except Exception as e:
            print(e)

    def send(chat_id, message, buttons=None):
        bot.send_message(chat_id, message, reply_markup=buttons)

    def send_diary_week(chat_id, diary):
        if diary != None:
            text, buttons = DairyController.print_diary_week(diary, chat_id)
            bot.send_message(chat_id, text, reply_markup=buttons)

    def send_diary_day(chat_id, datestr):

        text, buttons = DairyController.print_diary_day(datestr, chat_id)
        bot.send_message(chat_id, text, reply_markup=buttons)

    def send_diary_lesson(chat_id, lesson_name):
        text = DairyController.print_diary_lesson(lesson_name, chat_id)
        bot.send_message(chat_id, text)
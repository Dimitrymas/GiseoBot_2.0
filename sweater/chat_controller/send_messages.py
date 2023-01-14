import telebot
from telebot import types

from middlewares.user import MiddleUser
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

        if Im_user.g_password != None:
            buttons.add(types.KeyboardButton("Дневник"))
            buttons.add(types.KeyboardButton("Долги"))
            buttons.add(types.KeyboardButton("Почта"))
        else:
            buttons.add(types.KeyboardButton("Регистрация"))
        return buttons


class SendMessages:
    def send_start_message(chat_id):

        commands = [telebot.types.BotCommand("/start", "Перезапуск бота или смена данных учетной записи"),
                    telebot.types.BotCommand("/menu", "Меню"), telebot.types.BotCommand("/diary", "Дневник")]
        bot.set_my_commands(commands)
        buttons = SendButtons.drow_start_button()
        bot.send_message(chat_id, "Привет я бот, у которого ты можешь узнать о своих оценках", reply_markup=buttons)

    def send_menu(chat_id):
        try:
            buttons = SendButtons.drow_menu_buttons(chat_id)
            bot.send_message(chat_id, "Меню:", reply_markup=buttons)
        except:
            pass

    def send(chat_id, message, buttons=None):
        bot.send_message(chat_id, message, reply_markup=buttons)

    def send_diary_week(chat_id, diary):

        text, buttons = DairyController.print_diary_week(diary, chat_id)

        bot.send_message(chat_id, text, reply_markup=buttons, parse_mode='Markdown')

    def send_diary_day(chat_id, datestr):
        text, buttons = DairyController.print_diary_day(datestr, chat_id)
        bot.send_message(chat_id, text, reply_markup=buttons, parse_mode='Markdown')

    def send_diary_lesson(chat_id, lesson_name):

        text = DairyController.print_diary_lesson(lesson_name, chat_id)
        if text is not None:
            bot.send_message(chat_id, text, parse_mode='Markdown')
        else:
            bot.send_message(chat_id, "Не верная комманда, вы возвращенны в меню")
            SendMessages.send_menu(chat_id)

    def send_past_mand(chat_id, pastmand):
        buttons = types.ReplyKeyboardMarkup()
        buttons.add(types.KeyboardButton("Меню"))
        text = DairyController.print_past_mand(pastmand)
        if not text:
            text = 'Нет пропущенных заданий'
        bot.send_message(chat_id, text, reply_markup=buttons, parse_mode='Markdown')

    def send_mail(chat_id, mail):
        text, murkup = DairyController.print_mail(mail)

        murkup.add(types.KeyboardButton("Меню"))
        bot.send_message(chat_id, text, reply_markup=murkup, parse_mode='Markdown')

    def send_one_mail(chat_id, sender, theme, text, file_names, file_status):
        bot.send_message(chat_id, f"От *{sender}*\nТема: *{theme}*\nТекст: *{text}*\n *{file_status}*",
                         parse_mode='Markdown')
        for file_name in file_names:
            bot.send_document(chat_id, open(f'./files/{file_name}', 'rb'))

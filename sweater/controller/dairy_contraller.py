from telebot import types
from middlewares.time_convert import WeekTools as wt
from middlewares.user import MiddleUser


type_of_work = {39:"Самостоятельная работа"}


class DairyController:
    def print_day(printedText, wday):
        count = 0
        printedText += f"\n*{wt.curr_date(wday['date'])}*\n"

        for lessons in wday['lessons']:
            count += 1
            printedText += f"   _{count}) {lessons['subjectName']}_"
            mark = ' '
            if 'assignments' in lessons:
                for a in lessons['assignments']:
                    if 'mark' in a:
                        current_mark = str(a['mark']['mark'])
                        if current_mark == 'None':
                            current_mark = '🔴'
                        if mark != ' ':
                            mark += '  /  ' + current_mark
                        else:
                            mark += ' ' + current_mark
            if mark != ' ':
                printedText += '   — ' + mark + ' \n'
            else:
                printedText += ' \n'

        return printedText

    def print_diary_week(json, chat_id):

        if json != None:
            im_user = MiddleUser.get_user_by_chat(chat_id)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            printText = ""
            printedText = ""
            for wday in im_user.get_json_week()['weekDays']:
                printedText += (DairyController.print_day(printText, wday))
                button = types.KeyboardButton(wt.curr_day(wday['date']))
                markup.add(button)
            first = f"*{wt.curr_date(json['weekStart'])} по {wt.curr_date(json['weekEnd'])}*\n"
            button1 = types.KeyboardButton('Следующая неделя')

            button2 = types.KeyboardButton('Текущая неделя')

            button3 = types.KeyboardButton('Предыдущая неделя')

            markup.add(button3, button2, button1)

            markup.add(types.KeyboardButton('Меню'))
            return first+printedText, markup

    def print_diary_day(datestr, chat_id):

        im_user = MiddleUser.get_user_by_chat(chat_id)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        printedText = ""
        printText = ""
        for wday in im_user.get_json_week()['weekDays']:

            if wday["date"] == datestr:
                im_user.create_json_day(wday)
                printedText += (DairyController.print_day(printText, wday))
                for lessons in wday["lessons"]:
                    button = types.KeyboardButton(lessons['subjectName'])
                    markup.add(button)
        button = types.KeyboardButton("Выбор дня")
        markup.add(button)
        return printedText, markup

    def print_diary_lesson(lesson_name, chat_id):
        im_user = MiddleUser.get_user_by_chat(chat_id)
        wday = im_user.get_json_day()
        if wday != "error":
            for lessons in wday['lessons']:
                if lessons['subjectName'] == lesson_name:
                    mark = ' '
                    if 'assignments' in lessons:
                        for assignments in lessons['assignments']:
                            if 'mark' in assignments:

                                current_mark = str(assignments['mark']['mark'])
                                if current_mark == 'None':
                                    current_mark += '🔴'
                                if mark != ' ':
                                    mark += '  /  ' + current_mark
                                else:
                                    mark += ' ' + current_mark

                            printedText = f"{lesson_name} {mark}\n{assignments['assignmentName']}"
                        return printedText
                    else:
                        return "Не задано"
        else:
            return None


    def print_past_mand(pastmand):
        printedText = ""

        for m in pastmand:
            type = "Неизвестный тип работы"
            subjectName = m['subjectName']
            if type in type_of_work.keys():
                type = type_of_work[m['typeId']]
            assignmentName = m['assignmentName']
            date = wt.curr_date(str(m['dueDate']))

            printedText += f"*{subjectName} {type}* \n{assignmentName}\nДата сдачи: {date}\n\n"

        return printedText

    def print_mail(mail):
        murkup = types.ReplyKeyboardMarkup()
        printedText = ""
        count = 0
        for one_mail in mail["Records"]:
            if count == 10:
                break
            count += 1
            theme = one_mail["Subj"]
            if theme == '':
                theme = 'Не указана'

            from_name = one_mail['FromName']

            number = one_mail['MessageId']

            sent_date = one_mail['Sent']

            to_name = one_mail['SentTo']

            if one_mail['Read'] == 'Y':
                read = 'Да'
            else:
                read = 'Нет'

            printedText += f'*{count}) Номер сообщения:{number}*\n        _Тема: {theme}\n        От: {from_name}\n        Для:{to_name}\n        Дата отправки: {sent_date}\n        Прочитано: {read }_\n\n'

            murkup.add(types.KeyboardButton(f"{theme} ({number})"))



        if printedText == "":
            printedText = 'Сообщения не найдены'


        return printedText, murkup





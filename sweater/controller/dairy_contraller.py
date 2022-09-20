from telebot import types
from middlewares.time_convert import WeekTools as wt
from middlewares.user import MiddleUser

class DairyController:
    def print_day(printedText, wday):
        printedText += f"{wt.curr_date(wday['date'])}\n"
        for lessons in wday['lessons']:
            printedText += '*' + lessons['subjectName'] + '*'
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
            for wday in im_user.create_json_week(json)['weekDays']:
                printedText += (DairyController.print_day(printText, wday))
                button = types.KeyboardButton(wt.curr_day(wday['date']))
                markup.add(button)

            button1 = types.KeyboardButton('Следующая неделя')

            button2 = types.KeyboardButton('Текущая неделя')

            button3 = types.KeyboardButton('Предыдущая неделя')

            markup.add(button3, button2, button1)
            return printedText, markup

    def print_diary_day(datestr, chat_id):

        im_user = MiddleUser.get_user_by_chat(chat_id)
        print(datestr)
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

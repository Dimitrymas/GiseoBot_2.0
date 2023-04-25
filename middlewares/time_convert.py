import time
from datetime import datetime, timedelta, date

weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
month_list = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля', 'августа', 'сентября', 'октября', 'ноября',
              'декабря']
lessons = ["Иностранный язык (английский)", "История России. Всеобщая история", "Геометрия", "Физика", "Русский язык",
           "Родной язык (русский)", "География", "Биология", "Физическая культура", "Литература", "Информатика",
           "Алгебра", "Обществознание", "Химия", "Основы безопасности жизнедеятельности", 'Родная литература (русская)']


class WeekTools:
    def start_week(ddate):
        ret = datetime.strptime('%04d-%02d-1' % (ddate.year, ddate.isocalendar()[1]), '%Y-%W-%w')
        if date(ddate.year, 1, 4).isoweekday() > 4:
            ret -= timedelta(days=7)
        return ret

    def end_week(ddate):
        ret = WeekTools.start_week(ddate)
        return (ret + timedelta(days=6))

    def date_to_second(ddate):
        return (ddate.date() - date(1970, 1, 1)).total_seconds()

    def minus_week(this_week):
        this_week -= timedelta(days=7)
        return this_week

    def plus_week(this_week, weeks=1):
        this_week += timedelta(days=7 * weeks)
        return this_week

    def to_unix_time(c_date):
        return datetime.timestamp(c_date)

    def curr_date(cdate):
        cdate_splited = WeekTools.stringdate_to_mass(cdate)
        mounth = month_list[int(cdate_splited[1]) - 1]
        day = cdate_splited[2]
        year = cdate_splited[0]
        return f"{day} {mounth} {year} года"

    def stringdate_to_mass(cdate):
        cdate = cdate.split("T")[0]
        cdate_splited = cdate.split("-")
        return cdate_splited

    def curr_day(cdate):
        cdate_splited = WeekTools.stringdate_to_mass(cdate)
        datetime_str = f"{cdate_splited[2]}/{cdate_splited[1]}/{cdate_splited[0]}"
        datetime_object = datetime.strptime(datetime_str, '%d/%m/%Y')
        return f"{weekdays[datetime_object.weekday()]}({datetime_str})"

    def daydate_to_date(cdate):
        datetime_str = cdate.split("(")[1].split(")")[0]
        datetime_object = datetime.strptime(datetime_str, '%d/%m/%Y')
        return datetime_object

    def daydate_to_datestr(cdate):
        datetime_str = cdate.split("(")[1].split(")")[0].split("/")
        return f"{datetime_str[2]}-{datetime_str[1]}-{datetime_str[0]}T00:00:00"

    def datetime_to_sec(dt):
        microseconds = time.mktime(dt.timetuple()) * 1000000 + dt.microsecond
        return int(round(microseconds / float(1000000)))

    def datetime_diff_hour(start, end):
        return (WeekTools.datetime_to_sec(end) - WeekTools.datetime_to_sec(start)) > 3600

    def is_day_button(message):
        if message.split("(")[0] in weekdays:
            return True
        else:
            return False

    def is_lesson_button(message):
        return message in lessons

    def is_mail_button(message):

        if message.find("(") != -1 and len(message.split("(")[1]) == 9:
            return True
        else:
            return False

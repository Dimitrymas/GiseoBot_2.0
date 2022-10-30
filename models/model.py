from datetime import datetime, time
from sqlalchemy import Column, Integer, ForeignKey, String, Numeric, DateTime
from sqlalchemy_mixins.activerecord import ActiveRecordMixin
from sqlalchemy_mixins.repr import ReprMixin
from middlewares.time_convert import WeekTools as wt
from sweater import engine, Base, session

from sweater.liibs.giseo import Manager

managers = {}
weeks = {}
jsons_week = {}
jsons_day = {}

class BaseModel(Base, ActiveRecordMixin, ReprMixin):
    __abstract__ = True
    __repr__ = ReprMixin.__repr__
    pass

class City(BaseModel):
    __tablename__ = "city"
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(120))


class School(BaseModel):
    __tablename__ = "school"
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(120))
    city_id = Column(Integer, ForeignKey(City.id))


class User(BaseModel):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    g_name = Column(String(120))
    g_password = Column(String(120))
    role = Column(String(15), default="USER")
    telegram_id = Column(Numeric(15), unique=True)
    last_connect = Column(DateTime, nullable=True)
    school_id = Column(Integer, ForeignKey(School.id))
    last_week = Column(DateTime, nullable=True)


    def connectToGiseo(self):
        if Manager(login="Маслаков", password="415678", school_id="8", city_id="168") == "error":
            return "server_error"

        now = datetime.now()
        city_id = School.find(self.school_id).city_id
        if self.id not in managers or wt.datetime_diff_hour(self.last_connect, now) or managers[self.id].token == "":
            managers[self.id] = Manager(login=self.g_name, password=self.g_password, school_id=str(self.school_id), city_id=str(city_id))
            print(managers[self.id])
            if managers[self.id].token != "":
                self.update(last_connect=now)
                return managers[self.id]
            else:
                return "error"
        else:
            return managers[self.id]




    def get_diary(self):
        c_date = self.get_week()
        
        manager = self.connectToGiseo()

        if manager != "error" and manager != "server_error":

            diary = manager.getDiary(c_date)
            self.create_json_week(diary)
            return diary
        else:
            return manager

    def get_pastmandory(self):
        c_date = datetime.today()

        manager = self.connectToGiseo()

        if manager != "error" and manager != "server_error":
            pastmand = manager.getPastMandatory(c_date)
            return pastmand
        else:
            return manager





    def get_day(self, c_date):
        manager = self.connectToGiseo()
        return manager.getDiary(c_date)

    def get_week(self):
        now = datetime.now()
        if self.id not in weeks or wt.datetime_diff_hour(self.last_week, now):
            weeks[self.id] = now
            self.update(last_week=now)
        return weeks[self.id]

    def set_week(self, what):
        if what == "minus":
            weeks[self.id] = wt.minus_week(self.get_week())
        if what == "plus":
            weeks[self.id] = wt.plus_week(self.get_week())
        if what == "that":
            weeks[self.id] = datetime.now()

    def get_json_week(self):
        try:
            w = jsons_week[self.id]
        except Exception as e:
            self.get_diary()
            w = jsons_week[self.id]
        return w
    def create_json_week(self, json):
        jsons_week[self.id] = json
        return json

    def get_json_day(self):
        try:
            return jsons_day[self.id]
        except:
            return "error"


    def create_json_day(self, json):
        jsons_day[self.id] = json

    def get_mail(self):
        manager = self.connectToGiseo()

        if manager != "error":
            mail = manager.getMail()
            return mail
        else:
            return None

    def get_one_mail(self, number):
        manager = self.connectToGiseo()

        if manager != "error":
            theme, text, file, filename = manager.getOneMail(number)
            return theme, text, file, filename
        else:
            return None


Base.metadata.create_all(engine)
BaseModel.set_session(session)

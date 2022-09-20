from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, scoped_session
from config import *
import telebot

from sweater.liibs.giseo import Manager

engine = create_engine(DB)
Session = sessionmaker(bind=engine)
session = scoped_session(sessionmaker(bind=engine, autocommit=True))
Base = declarative_base()
bot = telebot.TeleBot(TG_TOKEN, parse_mode=None)


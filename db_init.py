import json

import requests

from models.model import *


def AddScools(s_json, city_id):
    schools_json = json.loads(s_json)
    for schools in schools_json.get("items"):
        School.create(id=schools["id"], name=schools["name"], city_id=city_id)


cities_json = json.loads(requests.get("https://giseo.rkomi.ru/webapi/prepareloginform").text).get("provinces")

for city in cities_json:
    if city["id"] < 0:
        id = str(city["id"])[1::]
        City.create(id=int(id), name=city["name"])

cities = City.all()

for city in cities:
    AddScools(requests.get(
        f"https://giseo.rkomi.ru/webapi/loginform?cid=2&sid=11&pid=-{city.id}&cn={city.id}&sft=2&LASTNAME=sft").text,
              city.id)

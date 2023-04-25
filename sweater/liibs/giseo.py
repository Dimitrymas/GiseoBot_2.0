import hashlib
import json
import time
import urllib

import requests

from middlewares.time_convert import WeekTools as wt


def md5(string: str):
    return hashlib.md5(string.encode()).hexdigest()


class Manager:
    # token for accessing giseo.rkomi.ru (default null)
    token: str = ''
    # cookies, https://developer.mozilla.org/ru/docs/Web/HTTP/Cookies
    cookies: dict = {}

    def __init__(self, login: str, password: str, school_id: str, city_id: str):
        self.login = login
        self.password = password
        self.school_id = school_id
        self.city_id = city_id

        self.auth()
        self.studentId = self.getStudentId()

    def send(self, path: str, method: str = 'GET', params: dict = {}, contentType: str = 'x-www-form-urlencoded',
             headers: dict = {}, withToken: bool = True, returnJson: bool = True):
        """
        Sending the request to https://giseo.rkomi.ru/webapi
        Parameters
        ----------
        path: str
          path to webapi (PATH_HERE -> https://giseo.rkomi.ru/webapi/PATH_HERE)

        method: str = GET
          method of request, GET or POST

        params: dict = {}
          request params

        contentType: str = x-www-form-urlencoded
          Content Type used in request headers, for example json or x-www-form-urlencoded

        headers: dict = {}
          request headers

        withToken: bool = True
          if token is need in request, set withToken to True

        returnJson: bool = True
          convert response to JSON and return it, otherwise return response
        """
        with requests.Session() as session:
            cookie: list[str] = []
            for name, value in self.cookies.items():
                cookie.append(f'{name}={value}')

            # https://developer.mozilla.org/ru/docs/Web/HTTP/Headers
            session.headers = {
                **headers,
                'at': self.token if withToken else None,
                'content-type': f'application/{contentType}; charset=UTF-8',
                # cookies are required to access certain addresses
                'cookie': '; '.join(cookie),
                'origin': 'https://giseo.rkomi.ru',

            }

            if method == 'GET':
                res = session.get(f'https://giseo.rkomi.ru/webapi/{path}', params=params)
            elif method == 'POST':
                res = session.post(f'https://giseo.rkomi.ru/webapi/{path}', data=urllib.parse.urlencode(
                    params) if contentType == 'x-www-form-urlencoded' else json.dumps(params))

            if (res.status_code == 200):
                # get new cookies from 'set-cookie' header from response and update self.cookies dictionary
                # Set-Cookie header: https://developer.mozilla.org/ru/docs/Web/HTTP/Headers/Set-Cookie
                self.cookies.update(res.cookies.get_dict())
                return res.json() if returnJson else res

            elif (res.status_code == 401):
                self.auth()
                return self.send(path, method, params, contentType, headers, withToken, returnJson)
            elif (res.status_code == 409):
                return "error"

    def auth(self):
        res: dict = self.send('auth/getdata', 'POST', {}, 'x-www-form-urlencoded',
                              {'Referer': 'https://giseo.rkomi.ru/about.html'}, False, True)
        password = md5(res['salt'] + md5(self.password))
        post_data = {
            'LoginType': '1',
            'cid': '2',
            'sid': '11',
            'pid': f'-{self.city_id}',
            'cn': self.city_id,
            'sft': '2',
            'scid': self.school_id,
            'UN': self.login,
            'PW': password[:len(self.password)],
            'lt': res['lt'],
            'pw2': password,
            'ver': res['ver']
        }

        data = self.send('login', 'POST', post_data, 'x-www-form-urlencoded',
                         {'Referer': 'https://giseo.rkomi.ru/about.html'}, False, True)
        if data != "error":
            self.token = data['at']
            self.ver = res['ver']

    def getDiary(self, anydate):
        """
          Getting Diary records
          Parameters
          ----------
          start: int
            start day of needed diary in UNIX time

          end: int
            end day of needed diary in UNIX time

          assigns: bool = False
            if assigns setted to True, they will also return
        """

        start_week = wt.start_week(anydate)

        end_week = wt.end_week(anydate)

        sDate = time.localtime(wt.to_unix_time(start_week))
        eDate = time.localtime(wt.to_unix_time(end_week))
        try:
            data = {
                'studentId': self.studentId,
                'vers': self.ver,
                'weekStart': f'{sDate.tm_year}-{str(sDate.tm_mon).zfill(2)}-{str(sDate.tm_mday).zfill(2)}',
                'weekEnd': f'{eDate.tm_year}-{str(eDate.tm_mon).zfill(2)}-{str(eDate.tm_mday).zfill(2)}',
                'yearId': 79783,
                'withLaAssigns': False
            }

            return self.send('student/diary', 'GET', data)
        except:
            return None

    def getLessonAttachment(self, assignsId):
        """
        Getting attachments of specified assigns IDs
        Parameters
        ----------
        assignsIds: list[int]
          ID of assign
        """

        return self.send(f'student/diary/get-attachments?studentId={self.studentId}', 'POST', {
            'assignId': [assignsId]
        }, 'json', returnJson=False).json()

    def getAttachments(self, file_id, file_name):
        print(file_name)
        """
        Getting attachments of specified assigns IDs
        Parameters
        ----------
        assignsIds: list[int]
          ID of assign
        """

        return self.send(f'attachments/{file_id}', 'GET', {
            "filename": file_name
        }, 'json', returnJson=False).content

    def getPastMandatory(self, anydate):
        """
        Получение пропущенных заданий
        Parameters
        ----------
        start: int
          start day of needed diary in UNIX time

        end:int
          end day of needed diary in UNIX time

        Возвращает
        ----------
          массив просроченных заданий
        """

        start_week = wt.start_week(anydate)

        end_week = wt.end_week(anydate)

        sDate = time.localtime(wt.to_unix_time(start_week))

        eDate = time.localtime(wt.to_unix_time(end_week))

        try:
            data = {
                'studentId': self.studentId,
                'weekStart': f'{sDate.tm_year}-{str(sDate.tm_mon).zfill(2)}-{str(sDate.tm_mday).zfill(2)}',
                'weekEnd': f'{eDate.tm_year}-{str(eDate.tm_mon).zfill(2)}-{str(eDate.tm_mday).zfill(2)}',
                'yearId': 79783
            }

            return self.send('student/diary/pastMandatory', 'GET', data, 'json')
        except:
            return None

    def getStudent(self):
        return self.send('student/diary/init', 'GET')

    def getStudentId(self):
        s = self.getStudent()

        if s != None:
            return s['students'][0]['studentId']

    def getMail(self):
        json_data = {"filterContext": {
            "selectedData": [
                {
                    "filterId": "MailBox",
                    "filterValue": "Inbox",
                    "filterText": "Входящие"
                }
            ]
        },
            "fields": [
                "author",
                "subject",
                "sent"
            ],
            "page": 1,
            "pageSize": 5,
            "search": None,
            "order": None
        }
        mail = self.send('mail/registry', params=json_data, method='POST', contentType='json', returnJson=True)
        return mail['rows']

    def getOneMail(self, id):
        files = {}
        mail = self.send(f'mail/messages/{id}/read?userId={self.studentId}', 'GET')
        sender = mail['author']['name']
        theme = mail['subject']
        text = mail['text']
        for file in mail['fileAttachments']:
            file_id = file['id']
            file_name = file['name']
            files[file_name] = self.getAttachments(file_id=file_id, file_name=file_name)

        return sender, theme, text, files

    def logout(self):
        self.send('auth/logout', 'POST', {'at': self.token, "VER": self.ver}, 'x-www-form-urlencoded', {}, False, False)

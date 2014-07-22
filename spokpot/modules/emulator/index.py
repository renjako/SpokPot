# import os
from jinja2 import Environment, PackageLoader, Template
import mimetypes
import random
# from modules.database.sqlite import init_db, db_session
# from modules.models.intext import Intext
# from modules.models.intitle import Intitle

import sqlite3

class IndexDork():
    def __init__(self):
        self.filetype = ''
        # template = Template()
        # env = Environment(loader=PackageLoader('yourapplication', 'templates'))
        
    def getFileType(self):
        return self.filetype

    def setFileType(self, value):
    	self.filetype = value

    def generateBody(self):
        

        conn = sqlite3.connect('0306.db')
        cursor = conn.cursor()
        # a = random.randrange(1,3)
        # if a ==1:
        #     thefile = 'modules/emulator/data/index/index.html'
        # else:
        #     thefile = 'modules/emulator/data/index/index2.html'
        # self.setFileType(mimetypes.guess_type(thefile)[0])
        # thefile = 'modules/emulator/data/index/index3.html'
        # self.filetype = mimetypes.guess_type(thefile)[0]
        # return open(thefile, 'rb').read()
        thefile = 'modules/emulator/data/index/indexspok.html'
        self.filetype = mimetypes.guess_type(thefile)[0]
        body = open(thefile, 'r').read()
        template = Template(body)

        cursor.execute("select * from intitle order by RANDOM() LIMIT 1")
        page_title = cursor.fetchone()
        bodystr = cursor.execute("select * from intext order by RANDOM()")
        return template.render(page_title=page_title, bodystr=bodystr).encode('utf-8')

    def sendCss(self):
        thefile = 'modules/emulator/data/style/style.css'
        self.setFileType(mimetypes.guess_type(thefile)[0])
        return open(thefile,'rb').read()

    def sendFavicon(self):
        thefile = 'modules/emulator/data/favicon/favicon.ico'
        self.setFileType(mimetypes.guess_type(thefile)[0])
        return open(thefile, 'rb').read()



# a = IndexDork()
# a.generateBody()
# print(type(a.sendCss()))
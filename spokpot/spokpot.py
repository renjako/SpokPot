import sys
import os
import time
import re
from datetime import datetime
from cgi import parse_qs
from http.server import BaseHTTPRequestHandler, CGIHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

from modules.database.sqlite import init_db, db_session
from modules.models.event import Event
from modules.classifier import Classifier


class SpokPot(CGIHTTPRequestHandler):
    sys_version = ''
    server_version = 'Apache/2.0.48'

    # def __init__(self):
    #     self.init_db()

    def do_GET(self):
        requestURI = self.path
        whatami = Classifier()
        body = whatami.spokme(requestURI)
        self.send_response(200)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Content-type', whatami.getFileType())
        self.writeDB(whatami.getPattern(), whatami.getFile())
        # print('iki header '+str(self.headers))
        self.end_headers()
        self.wfile.write(body)

    def writeDB(self, pattern, filename):

        event = Event()
        event.time = self.log_date_time_string()
        if self.headers['X-Forwarded-For'] and self.validateIPv4(self.headers['X-Forwarded-For']):
            event.source = self.headers['X-Forwarded-For']
        else:
            event.source = str(self.address_string())
        event.request_url = self.path
        event.request_raw = self.command + ' ' + self.path + ' ' + self.request_version + '\n' + str(self.headers)
        event.pattern = pattern
        

        event.filename = filename
        db_session.add(event)
        
        try:
            db_session.commit()
        except:
            db_session.rollback()
        finally:
            db_session.close()

    def do_POST(self):
        self.do_GET()

    def log_message(self, format, *args):
        thefile = 'coba.log'
        if self.headers['X-Forwarded-For']:
            ipbro = self.headers['X-Forwarded-For']
        else:
            ipbro = str(self.address_string()) 

        sys.stderr.write("%s - [%s] %s\n" %
            (ipbro,
                self.log_date_time_string(),
                format%args))


        with open(thefile, 'a+') as tulis:
            tulis.write(ipbro+' '+self.log_date_time_string()+' '+format%args+'\n')


    def log_date_time_string(self):
        dt_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return dt_string

    def validateIPv4(self, ip):
        ip_regex = "^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$";
        match = re.search(ip_regex, ip)
        if match:
            return True
        else:
            return False


class ThreadServer(ThreadingMixIn, HTTPServer):
    """run baby run run"""
port = 80
httpd = ThreadServer(('',port),SpokPot)
# honeypot = SpokPot()
# httpd = make_server('', 8000, honeypot)
print("Serving on port " + str(port) + "...")
init_db()
# Serve until process is killed
httpd.serve_forever()

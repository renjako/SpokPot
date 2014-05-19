import sys
import os
from cgi import parse_qs
from modules.classifier import Classifier 
# Every WSGI application must have an application object - a callable
# object that accepts two arguments. For that purpose, we're going to
# use a function (note that you're not limited to a function, you can
# use a class for example). The first argument passed to the function
# is a dictionary containing CGI-style envrironment variables and the
# second variable is the callable object (see PEP 333).

"""
class SpokPot:
    def __call__(self, environ, start_response):
        # construct uri of request
        requestURI = environ.get('PATH_INFO')
        if environ.get('QUERY_STRING'):
        	requestURI += '?' + environ.get('QUERY_STRING')
        print(requestURI)

        whatami = Classifier()

        attack = whatami.spokme(requestURI)
        # print(attack)
        determiner = AttackHandler()

        # print(type(determiner.determine(attack)))


        # The returned object is going to be printed
        body = determiner.determine(attack).encode()
        # if isinstance(body, str):
        #     body.encode()
        status = '200 OK' # HTTP Status
        headers = [('Content-type', determiner.getFileType() )] # HTTP Headers
        start_response(status, headers)

        # return [b'hallo']
        # print(type(body))
        return [body]
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
class SpokPot(BaseHTTPRequestHandler):
    sys_version = ''
    server_version = 'Apache/2.0.48'
    def do_GET(self):
        requestURI = self.path
        whatami = Classifier()
        body = whatami.spokme(requestURI)
        self.send_response(200)
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Content-type', whatami.getFileType())
        print(whatami.getFileType())
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        self.send_response(200)
        self.wfile.write(b'this is post')

    def log_message(self, format, *args):
        thefile = 'coba.log'
        sys.stderr.write("%s - - [%s] %s\n" %
            (self.address_string(),
                self.log_date_time_string(),
                format%args))
        with open(thefile, 'a+') as tulis:
            tulis.write(self.address_string()+' '+self.log_date_time_string()+' '+format%args+'\n')

class ThreadServer(ThreadingMixIn, HTTPServer):
    """run baby run run"""

httpd = ThreadServer(('',8000),SpokPot)

# honeypot = SpokPot()
# httpd = make_server('', 8000, honeypot)
print("Serving on port 8000...")

# Serve until process is killed
httpd.serve_forever()

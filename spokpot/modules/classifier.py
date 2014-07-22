import re
import urllib.parse
from modules.emulator.index import IndexDork
from modules.emulator.lfi import LocalFileInclusion
from modules.emulator.rfi import RemoteFileInclusion
from modules.emulator.pma import PhpMyAdminEmu
from modules.emulator.phpinfo import PHPinfo

class Classifier():
    """
    this is the regex to determine the type of attack/request
    """

    regex_rfi = '.*(=.*(http(s){0,1}|ftp(s){0,1}):).*'
    regex_php_inj = '.*(define|eval|file_get_contents|include|require|require_once|set|shell_exec|phpinfo|system|passthru|preg_|execute|echo|print|print_r|var_dump|[fp]open)\(.*'
    regex_php = '.*(<\?php).*'
    regex_sql_benchmark = '.*((select|;)\s+(benchmark|if|sleep)).*'
    regex_sqli = '.*(select|drop|update|union|insert|alter|declare|cast)( |\().*'
    regex_html_inj = '.*(<|%3c)(frame|applet|isindex|marquee|keygen|script|audio|video|input|button|textarea|style|base|body|meta|link|object|embed|param|plaintext|xml|image).*'
    regex_xml_entity = '.*(element|entity|\[CDATA).*'
    regex_basic_xss = '.*(alert|eval|msgbox|showmodaldialog|prompt|write|confirm|dialog|open).*'
    regex_js_properties = '.*(hash|href|navigateandfind|source|pathname|close|constructor|port|protocol|assign|replace|back|forward|document|ownerdocument|window|self|parent|frames|cookie|innerhtml|innertext|resizeto|createstylesheet)\(.*'
    regex_lfi = '\?.*(/\.\.)*(home|conf|usr|etc|proc|opt|s?bin|local|dev|tmp|kern|root|sys|system|windows|winnt|program|inetpub/boot\.ini)/.*'
    regex_lfi_win = '\?.*[a-zA-Z]:((([\\/]+(.{0,2}))|[\\/]+)[^\\/:*?"<>|,]+)+.*'
    regex_xss = '.*(script).*'
    regex_favicon = '.*(favicon.ico).*'
    regex_css = '.*/style\.css$'
    regex_robot = '^/robots\.txt$'
    regex_pma = '(^/phpmyadmin|^/pma|^/phpmyadmin\-[\w\.]+)'
    regex_comment_spam = '.*/comments'
    regex_login = '^/login'
    regex_tomcat_man = '^/manager/html'
    regex_tomcat_stat = '^/manager/status'
    regex_phpinfo = '^/info.php|^/phpinfo.php|^/phpinfo.html'
        
    def __init__(self):
            self.fileType = 'iki loh'
            self.pattern = ''
            self.filename = ''

    def spokme(self, requestURI):

        # line = 'aldo.com/style.css?=http://'
        # check regex match
        # hasil = re.search(self.regex_css, line, re.IGNORECASE)
        # print(hasil)  

        # classification of the request
        requestURI = urllib.parse.unquote(requestURI)
        result = ''
        for pattern in (self.regex_rfi, self.regex_php, self.regex_sqli, self.regex_php, self.regex_lfi, self.regex_favicon, self.regex_css, self.regex_robot, self.regex_login, self.regex_tomcat_man, self.regex_tomcat_stat, self.regex_pma, self.regex_phpinfo):
            match = re.search(pattern, requestURI, re.IGNORECASE)
            # print(type(match))
            if match:
                
                if pattern == self.regex_rfi:
                    print('RFI')
                    self.setPattern('rfi')
                    result = self.rfi(requestURI)
                    break
                elif pattern == self.regex_php:
                    print('php')
                    self.setPattern('php')
                    result = self.php()
                    break
                elif pattern == self.regex_sqli:
                    print('SQL Injection')
                    self.setPattern('sqli')
                    result = self.sqli()
                    break
                elif pattern == self.regex_lfi:
                    print('LFI')
                    self.setPattern('lfi')
                    result = self.lfi(requestURI)
                    break
                elif pattern == self.regex_favicon:
                    self.setPattern('favicon')
                    result = self.favicon()
                    break
                elif pattern == self.regex_css:
                    self.setPattern('style_css')
                    result = self.css()
                    break
                elif pattern == self.regex_robot:
                    print('robots')
                    self.setPattern('robots')
                    result = self.robot()
                    break
                elif pattern == self.regex_pma:
                    print('phpmyadmin')
                    self.setPattern('phpmyadmin')
                    result = self.pma(requestURI)
                    break
                elif pattern == self.regex_login:
                    print('login')
                    self.setPattern('login')
                    result = self.login()
                    break
                elif pattern == self.regex_tomcat_man:
                    print('tomcat manager')
                    self.setPattern('tomcat manager')
                    result = self.login()
                    break
                elif pattern == self.regex_tomcat_stat:
                    print('tomcat status')
                    self.setPattern('tomcat status')
                    result = self.login()
                    break
                elif pattern == self.regex_phpinfo:
                    print('phpinfo')
                    self.setPattern('phpinfo')
                    result = self.phpinfo()
                    break
                else:
                    break
            elif pattern == self.regex_phpinfo:
                print('unknown')
                self.setPattern('unknown')
                result = self.dork()

        return result

    def setPattern(self, value):
        self.pattern = value

    def getPattern(self):
        return self.pattern

    def setFile(self, value):
        self.filename = value

    def getFile(self):
        return self.filename

    def setFileType(self, value):
        self.fileType = value

    def getFileType(self):
        return self.fileType

    def rfi(self, requestURI):
        includer = RemoteFileInclusion()
        result = includer.handle(requestURI)
        if result != None:
            self.setFile(result[1])
            return result[0]
        else:
            return result

    def sqli(self):
        # print('we dont have sqli')
        return self.dork()

    def php(self):
        # print('we no run php')
        return self.dork()

    def lfi(self, requestURI):
        includer = LocalFileInclusion()
        result = includer.handle(requestURI)
        self.fileType = includer.getFileType()
        return result

    def favicon(self):
        # print('wth is favicon')
        dorker = IndexDork()
        result = dorker.sendFavicon()
        self.setFileType(dorker.getFileType())
        return result

    def css(self):
        # print('do we need css?')
        dorker = IndexDork()
        result = dorker.sendCss()
        self.setFileType(dorker.getFileType())
        return result
        
    def robot(self):
        # print('are we in the future?')
        return self.dork()


    def pma(self, requestURI):
        pma = PhpMyAdminEmu()
        return pma.handle(requestURI)  

    def login(self):
        return self.dork()

    def tomcat_man(self):
        return self.dork()

    def tomcat_stat(self):
        return self.dork()

    def phpinfo(self):
        phpinfoer = PHPinfo()
        result = phpinfoer.handle()
        self.fileType = phpinfoer.getFileType()
        return result

    def dork(self):
        dorker = IndexDork()
        result = dorker.generateBody()
        self.setFileType(dorker.getFileType())
        return result  

# spoker = Classifier()
# print(spoker.spokme('/robots.txt '))
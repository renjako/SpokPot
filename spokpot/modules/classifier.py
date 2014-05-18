import re
from modules.emulator.index import IndexDork
from modules.emulator.lfi import LocalFileInclusion

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
        
    def __init__(self):
            self.fileType = 'iki loh'

    def spokme(self, requestURI):

        # line = 'aldo.com/style.css?=http://'
        # check regex match
        # hasil = re.search(self.regex_css, line, re.IGNORECASE)
        # print(hasil)  

        # classification of the request
        result = ''
        for pattern in (self.regex_rfi, self.regex_php, self.regex_lfi, self.regex_favicon, self.regex_css, self.regex_pma):
            match = re.search(pattern, requestURI, re.IGNORECASE)
            # print(type(match))
            if match:
                
                if pattern == self.regex_rfi:
                    result = self.rfi()
                elif pattern == self.regex_php:
                    result = self.php()
                elif pattern == self.regex_lfi:
                    result = self.lfi()
                elif pattern == self.regex_favicon:
                    result = self.favicon()
                elif pattern == self.regex_css:
                    result = self.css()
                elif pattern == self.regex_pma:
                    print('pma')
                else:
                    break
            elif pattern == self.regex_pma:
                result = self.dork()

        return result

    def setFileType(self, value):
        self.fileType = value

    def getFileType(self):
        return self.fileType

    def lfi(self):
        print('let me find the file for you')
        result = LocalFileInclusion.handle(self)

    def rfi(self):
        print('where the remote file location?')
        return 'rfi'

    def php(self):
        print('wait, i dont think i run php here?')
        return 'php'

    def pma(self):
        return 'pma'

    def dork(self):
        print('wth is your request')
        dorker = IndexDork()
        self.setFileType(dorker.getFileType())
        return dorker.generateBody()

    def favicon(self):
        print('wth is favicon')
        dorker = IndexDork()
        self.setFileType(dorker.getFileType())
        return dorker.sendFavicon()

    def css(self):
        print('do we need css?')
        dorker = IndexDork()
        self.setFileType(dorker.getFileType())
        return dorker.sendCss()
        


# spoker = Classifier()
# print(spoker.spokme('/robots.txt '))


# import os
import mimetypes

class IndexDork():
    def __init__(self):
        self.filetype = ''
    def getFileType(self):
    	return self.filetype

    def setFileType(self, value):
    	self.filetype = value

    def generateBody(self):
        thefile = 'modules/emulator/data/index/index.html'
        # self.setFileType(mimetypes.guess_type(thefile)[0])
        self.filetype = mimetypes.guess_type(thefile)[0]
        return open(thefile, 'rb').read()

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
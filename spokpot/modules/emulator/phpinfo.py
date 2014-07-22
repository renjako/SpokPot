import re
import os
import mimetypes

class PHPinfo():
	def __init__(self):
		"""init"""
		self.fileType = ''

	def getFileType(self):
		return self.fileType

	def handle(self):
		thefile = 'modules/emulator/data/phpinfo/phpinfo.html'
		self.filetype = mimetypes.guess_type(thefile)[0]
		return open(thefile, 'rb').read()

# lfi = LocalFileInclusion()
# print(lfi.handle('index.php?file=../../../../../../etc/passwd'))

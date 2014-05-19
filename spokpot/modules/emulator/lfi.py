import re
import os
import mimetypes

class LocalFileInclusion():
	def __init__(self):
		"""init"""
		self.fileType = ''

	def collectfiles(self):
		tree = []
		for root, subFolders, files in os.walk('modules/emulator/data/lfi/'):
			for dir_file in files:
				tree.append(os.path.join(root, dir_file))
		return tree

	def handle(self, uri):
		pattern = re.compile(r'(\.\./)*')
		localfile = pattern.split(uri.split('\0', 1)[0], maxsplit=1)
		path = os.path.join('modules/emulator/data/lfi', localfile[-1])
		try:
			if path in self.collectfiles():
				#print(self.collectfiles())
				self.filetype = mimetypes.guess_type(path)[0]
				result = open(path, 'rb').read()
				return result
			else:
				raise IOError
		except IOError:
			return b"Warning: include(vars1.php): failed to open stream: No such file or directory in /var/www/html/anonymous/test.php on line 6 Warning: include(): Failed opening 'vars1.php' for inclusion (include_path='.:/usr/share/pear:/usr/share/php') in /var/www/html/anonymous/test.php on line 6"

	def getFileType(self):
		return self.fileType

# lfi = LocalFileInclusion()
# print(lfi.handle('index.php?file=../../../../../../etc/passwd'))

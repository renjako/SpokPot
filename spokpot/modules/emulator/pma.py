import re
import os

class PhpMyAdminEmu():
	def __init__(self):
		"""init"""

	def collectfiles(self):
		tree = []
		for root, subFolders, files in os.walk('modules/emulator/data/phpmyadmin/'):
			for dir_file in files:
				tree.append(os.path.join(root, dir_file))
		return tree


	def handle(self, uri):
		pattern = re.compile(r'(\.\./)*')
		localfile = pattern.split(uri.split('/', 2)[-1], maxsplit=1)
		path = os.path.join('modules/emulator/data/phpmyadmin/', localfile[-1])
		print(path)
		print('------')
		print(self.collectfiles())
		try:
			if path in self.collectfiles():
				
				result = open(path, 'rb').read()
				return result
			else:
				raise IOError
		except IOError:
			result = open('modules/emulator/data/phpmyadmin/script_setup.php','rb').read()
			return result

# pma = PhpMyAdminEmu()
# (pma.handle('phpmyadmin/'))
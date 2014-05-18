import re
import os

class LocalFileInclusion():
	def collectfiles(self):
		tree = []
		for root, subFolders, files in os.walk('modules/emulator/data/lfi/'):
			for dir_file in files:
				tree.append(os.path.join(root, dir_file))
		return tree

	def handle(self, uri):
		pattern = re.compile(r'(\.\./)*')
		localfile = pattern.split(uri.split('\0', 1)[0], maxsplit=1)
		path = os.path.join('modules/emulator/data/lfi', localfile[2])
		try:
			if path in self.collectfiles():
				#print(self.collectfiles())
				result = open(path, 'rb').read()
				return result
			else:
				raise IOError
		except IOError:
			return 'no such'

#lfi = LocalFileInclusion()
#print(lfi.handle('index.php?file=../../../../../../etc/passwd'))
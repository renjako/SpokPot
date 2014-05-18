from modules.emulator.index import IndexDork
from modules.emulator.lfi import LocalFileInclusion

class AttackHandler():

	# def __init__(self):
	# 	
	def determine(self, attack):
		result = ''
		if attack == 'rfi':
			print('where the remote file location?')
		elif attack == 'php':
			print('wait, i dont think i run php here?')
		elif attack == 'lfi':
			print('let me find the file for you')
			result = LocalFileInclusion.handle(self)
		elif attack == 'favicon':
			print('wth is favicon')
			result = IndexDork.sendFavicon(self)
			self.setFileType(IndexDork.getFileType(self))
		elif attack == 'css':
			print('do we need css?')
			result = IndexDork.sendCss(self)
			self.setFileType(IndexDork.getFileType(self))
		elif attack == 'pma':
			print('gogo drop the table')
		else:
			print('i guess you just need dorkiporki')
			result = IndexDork.generateBody(self)
			self.setFileType(IndexDork.getFileType(self))
		
		return result

	def getFileType(self):
		return self.fileType

	def setFileType(self, value):
		self.fileType = value
	# def headergen(self)
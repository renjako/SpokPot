import urllib.request as req
import hashlib
import re
import os
import subprocess

# url = 'http://example.com/'
# response = urllib.request.urlopen(url)
# data = response.read()      # a `bytes` object
# text = data.decode('utf-8') # a `str`; this step can't be used if data is binary


class RemoteFileInclusion():
	def __init__(self):
		"""ASdasdasd"""

	def generateName(self, filespok):
		newname = hashlib.md5(filespok).hexdigest()
		return newname

	def saveFile(self, filespok):
		file_name = self.generateName(filespok)
		if not os.path.exists(os.path.join('modules/emulator/data/rfi/',file_name)):
			with open(os.path.join('modules/emulator/data/rfi/',file_name), 'w+') as downloaded:
				downloaded.write(self.overridPHP(filespok.decode('utf-8')))
		# print(os.path.join('modules/emulator/data/rfi/',file_name))
		return file_name

	def getFile(self, url):
		theurl = url.split('=')[1]
		# proxy = req.ProxyHandler({'http': r'http://202.46.129.19:8080'})
		# download = req.urlopen(theurl, timeout=4).read()
		try:
			download = req.urlopen(theurl, timeout=4).read()
		except IOError as e:
			print('io error')
			file_name = None
		except req.URLError as e:
			print('url')
			file_name = None
		else:
			# print('download')
			download = download
			file_name = self.saveFile(download)
		return file_name

	def sandbox(self, file_name):
		phpoverider = 'modules/emulator/data/rfi/rfi.php'
		infected_file = self.overridPHP('modules/emulator/data/rfi/'+file_name)
		proc = subprocess.Popen('php '+phpoverider+' '+infected_file, shell=True, stdout=subprocess.PIPE)
		script_response = proc.stdout.read()
		return script_response.decode('utf-8')

	def overridPHP(self, php):
		replacer = ['getcwd','getmygid','is_writable','function_exists','disk_free_space','system','exec','php_uname','disk_total_space','shell_exec','passthru','get_current_user','fsockopen','getenv','getmyuid','diskfreespace','ini_get','is_callable','popen']
		for replaced in replacer:
			php = php.replace(replaced, replaced+'_spok')
		return php
		# print(type(replacer[0][0]))

	def handle(self, uri):
		infected_file = self.getFile(uri)
		if infected_file != None:
			result = [self.sandbox(infected_file).encode('utf-8'), infected_file]
		else:
			error = "Warning: include(vars1.php): failed to open stream: No such file or directory in /var/www/html/anonymous/test.php on line 6 Warning: include(): Failed opening 'vars1.php' for inclusion (include_path='.:/usr/share/pear:/usr/share/php') in /var/www/html/anonymous/test.php on line 6"
			result = [error.encode('utf-8'),None]
		return result

# spok = RemoteFileInclusion()
# print(spok.handle('index.php?file=http://10.151.36.3/rfi2')[1])
# spok.handle('index.php?file=http://google.com')
# spok.sandbox('1edbc94bd1182417608bcc51f128d60e')
# spok.overridPHP('echo getcwd();')
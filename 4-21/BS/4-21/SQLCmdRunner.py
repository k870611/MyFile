import os, sys, re, time, argparse, random, logging, base64, hashlib, tempfile, subprocess
from os.path import expanduser
from Crypto import Random
from Crypto.Cipher import AES
from threading import Timer

import mysql
import mysql.connector

class SQLCmdRunner():
	__PERIOD = 60 * 10 # period of changing password
	__NOTIFY = 60 * 5 # the exceed time after last run
	__DATABASE = 'test'
	__IP = 'localhost'
	__TICKS = 10.0
	__SUBMITTICKS = 30.7 # 307 is a prime number

	__SQLCmdPrefix = 'CALL insert_[\w\_]\s'
	__COMMENT = r'(?:\#|\;|\/\*).*'
	# __VERBOSE = os.environ.get('_VERBOSE')
	# __DEBUG = os.environ.get('_DEBUG')
	# __UNSAFE = os.environ.get('_UNSAFE')

	USER = 'worker'
	PWDFile = os.path.join(expanduser('~'), 'password.txt') # str(os.path.home) for > 3.5
	PWDNewFile = os.path.join(expanduser('~'), 'password.txt.bak')
	SQLDir = os.path.join(tempfile.gettempdir(), 'results')

	def __init__(self):
		try:
			# self.__VERBOSE = os.environ.get('_VERBOSE')
			self.__DEBUG = os.environ.get('_DEBUG')
			self.__UNSAFE = os.environ.get('_UNSAFE')

			command = 'fltmc'

			if self.__UNSAFE:
				command = 'dir'

			fltmc = subprocess.check_output(command) # admin only command
			m5 = hashlib.md5()
			m5.update(fltmc)

			self.__key = m5.hexdigest()

			self.__lastrun = self._lastrun() # self._lastrun()
			self.__lastnotify = self.__lastrun - self.__PERIOD + self.__NOTIFY
			self.__lastconnect = 0
			self.__connection = None

		except:
			logging.error('No admin permission.')

	def _generate_password(self):
		return str(''.join([chr(random.randrange(65, 90)) for i in range(random.randrange(6,16))]))

	def _encrypt(self, pwd):
		iv = Random.new().read(AES.block_size)
		cipher = AES.new(self.__key, AES.MODE_CBC, iv)
		return base64.b64encode(iv + cipher.encrypt(pwd.rjust(16))).decode('utf-8')

	def _decrypt(self, enc):
		enc = base64.b64decode(enc)
		iv = enc[:AES.block_size]
		cipher = AES.new(self.__key, AES.MODE_CBC, iv)
		return cipher.decrypt(enc[AES.block_size:]).decode('utf-8').strip()

	def _lastrun(self,currenttime=None):
		if currenttime is None:
			currenttime = time.time()

		return int(currenttime/self.__PERIOD)*self.__PERIOD

	def _nextrun(self):
		return self.__lastrun + self.__PERIOD

	def _nextnotify(self):
		return self.__lastrun + self.__NOTIFY

	def _create(self, file, timestamp=None, encryptpwd=None):
		if timestamp is None:
			timestamp = self._lastrun()

		if encryptpwd is None:
			encryptpwd = self._encrypt(self._generate_password())

		while True:
			try:
				fh = open(file, 'w+')
				fh.write(encryptpwd)
				fh.close()
				os.utime(file, (timestamp, timestamp))
				break
			except:
				logging.error('Cannot write "{}" to {}'.format(encryptpwd, file))
				time.sleep(random.randrange(1,10)/10)
				pass

	def _overwrite_password(self):
		''' update the password file from op user '''
		try:
			if not os.path.isfile(self.PWDFile):
				raise Exception('Need root user to set the 1st password file')

			if not os.path.isfile(self.PWDNewFile):
				self._create(self.PWDNewFile, timestamp=self._nextnotify())
				return

			fh = open(self.PWDNewFile)
			encryptpwd = fh.readline().strip()
			fh.close()
			newpwd = self._decrypt(encryptpwd)

			fh = open(self.PWDFile)
			encryptpwd = fh.readline().strip()
			fh.close()
			curpwd = self._decrypt(encryptpwd)

			conn = mysql.connector.connect(user=self.USER, password=curpwd, database=self.__DATABASE, use_unicode=True)
			cursor = conn.cursor()
			cursor.execute("SET PASSWORD FOR '{}'@'{}' = '{}';".format(self.USER, self.__IP, newpwd))
			cursor.close()
			conn.close()

			self._create(self.PWDFile, timestamp=self._lastrun(), encryptpwd=encryptpwd)

		except Exception as ex:
			logging.error('Cannot connect to DB with the {}.  Error={}.'.format(self.USER, str(ex)))

	def _move_files(self):
		for file in os.listdir(self.SQLDir):
			if not file.endswith(".4"):
				continue

			filespec = os.path.join(self.SQLDir, file)
			newfile = filespec[:-1] + '5'
			completefile = filespec[:-1] + '6'

			try:
				os.rename(filespec, newfile)
				fh = open(newfile)
				lines = fh.readlines()
				fh.close()
			except:
				continue # next file

			try:
				cursor = self.__connection.cursor()

				for line in lines:
					if not line.startswith(self.__SQLCmdPrefix):
						continue

					line = re.sub(self.__COMMENT, ';', line).strip()
					if line != '':
						cursor.execute(line)

				self.__connection.commit()

				os.rename(newfile, completefile)

			except Exception as ex:
				if self.__connection:
					self.__connection.rollback()
				logging.error('Error %d: %s'.format(ex.args[0], ex.args[1]))

		if self.__connection:
			self.__connection.close()
			self.LoadConnection()

	def LoadConnection(self):
		try:
			latestupdate = os.path.getmtime(self.PWDFile)
			if ((self.__lastconnect < latestupdate) or (self.__connection is None)):
				fh = open(self.PWDFile)
				encrytpwd = fh.readline().strip()
				fh.close()
				if self.__DEBUG is None:
					self.__connection = mysql.connector.connect(user=self.USER, password=self._decrypt(encrytpwd), database=self.__DATABASE, use_unicode=True)
				else:
					print('mysql.connector.connect(user={},password={},database={}), lastupdate={}'.format(self.USER, self._decrypt(encrytpwd), self.__DATABASE, latestupdate))

				self.__lastconnect = latestupdate
		except:
			self.__connection = None

		return self.__connection

	def PasswordRenewer(self, times=None):
		''' renew the password if need '''
		currenttime = time.time()
		nextrun = self._nextrun()
		nextnotify = self._nextnotify()

		if currenttime >= nextrun:
			self._overwrite_password()
		elif currenttime >= nextnotify and self.__lastnotify != nextnotify:
			self._create(self.PWDNewFile, timestamp=nextnotify)
			self.__lastnotify = nextnotify

		if times is not None:
			times = times - 1

		if ((times is None) or (times > 0)):
			thetimer = Timer(self.__TICKS, self.PasswordRenewer, args=[self, times])
			thetimer.start()

		return

	def ResetPassword(self, rootuser, rootpwd, oppwd):
		''' reset password by root user '''
		try:
			conn = mysql.connector.connect(user=rootuser, password=rootpwd, database=self.__DATABASE, use_unicode=True)
			cursor = conn.cursor()
			cursor.execute("SET PASSWORD FOR '{}'@'{}' = '{}';".format(self.USER, self.__IP, oppwd))
			cursor.close()
			conn.close()

			self._create(self.PWDFile, timestamp=self._lastrun(), encryptpwd=self._encrypt(oppwd))
			self.pwd = oppwd

		except Exception as ex:
			logging.error('Cannot connect to DB with the {}.  Error={}'.format(rootuser, str(ex)))

	def Submit(self):
		if self.__connection is None:
			self.LoadConnection()
		else:
			self._move_files()

		thetimer = Timer(self.__SUBMITTICKS, self.Submit, [self])
		thetimer.start()


if __name__ == '__main__':
	# initialize
	parser = argparse.ArgumentParser(description='SQL Command Runner')

	parser.add_argument('--rootuser', action='store', nargs='?', default='admin')
	parser.add_argument('--rootpwd', action='store', nargs='?', default='admin')
	parser.add_argument('--oppwd', action='store', nargs='?', default='admin')
	parser.add_argument('--debug', action='store', nargs='?', default=os.environ.get('__DEBUG'))
	parser.add_argument('--unsafe', action='store', nargs='?', default=os.environ.get('__UNSAFE'))
	# parser.add_argument('--verbose', action='store', nargs='?', default=os.environ.get('__VERBOSE'))
	parser.add_argument('--version', action='version', version='%(prog)s v0.1')

	runner = SQLCmdRunner()

	# parse argument
	args = parser.parse_args()

	# os.environ['__VERBOSE'] = args.verbose
	os.environ['__DEBUG'] = args.debug
	os.environ['__UNSAFE'] = args.unsafe

	runner.ResetPassword(args.rootuser, args.rootpwd, args.oppwd)

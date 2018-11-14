import os, io, sys, re, csv, time, copy, json, subprocess, shlex, codecs, binascii, datetime, base64, logging, struct

def debug(msg):
	# print(msg)
	logging.debug(msg)

def info(msg):
	print(msg)
	logging.info(msg)

def error(msg):
	# print(msg)
	logging.error(msg)

def int_from_bytes(bytes, order):
	return struct.unpack('<L', bytes)[0] if order == 'little' else struct.unpack('>L', bytes)[0]
	
def int_to_bytes(value, length, order):
	seq = 1 if order == 'big' else -1
	result = ['\0'] * length
	while value > 0:
		length = length - 1
		ch = value % 256
		result[length] = chr(ch)
		value = int(value/256)
	return (''.join(result[::seq])).encode('utf-8')
	
def parseargs(syntax, theargs):
	def userusage():
		if 'USAGE' not in syntax:
			print(str(syntax))
		else:
			syntax['USAGE']()
		sys.exit(1)

	usage_arglist = ['USAGE', 'ARGLIST']
	for thekey in syntax.keys():
		if thekey not in usage_arglist:
			syntax[thekey][1] = syntax[thekey][2]

	pos = 0
	while pos < len(theargs):
		if theargs[pos] in syntax:
			thetype = syntax[theargs[pos]][0]
			if thetype is bool:
				syntax[theargs[pos]][1] = not syntax[theargs[pos]][1]
				pos = pos + 1
				continue 

			if thetype is int:
				syntax[theargs[pos]][1] = int(theargs[pos+1], 10)
			elif thetype is Hex:
				syntax[theargs[pos]][1] = int(theargs[pos+1], 16)
			elif thetype is str:
				syntax[theargs[pos]][1] = theargs[pos+1]
			pos = pos + 2
			continue

		if theargs[pos] == '-h':
			userusage()

		if 'ARGLIST' not in syntax:
			syntax['ARGLIST'] = []

		syntax['ARGLIST'].append(theargs[pos])
		pos = pos + 1

	for thekey in syntax.keys():
		if (thekey not in usage_arglist) and (syntax[thekey][3] is not None) and (syntax[thekey][1] == syntax[thekey][3]):
			error('Invalid value for ' + thekey)
			userusage()

	return syntax

class IPMIException(Exception):
	pass
	
class BinFileHeaderInvalidException(Exception): 
	pass

class BinFileFormatException(Exception): 
	pass

class BinFileExistException(Exception): 
	pass

class BinFileSubmitException(Exception):
	pass

class CFGFileException(Exception):
	pass
	
class Hex(int):
	NOTES = '0123456789ABCDEF'
	LITTLE = 'little'
	BIG = 'big'

	def __init__(self, value=0):
		self.value = value

	def __int__(self):
		return self.value

	def __str__(self):
		hexstr = (hex(self.value))[2:].upper()
		return (hexstr if len(hexstr)&1 == 0 else ('0' + hexstr))

	def __repr__(self):
		hexstr = (hex(self.value))[2:].upper()
		return (('0x'+hexstr) if len(hexstr)&1 == 0 else ('0x0' + hexstr))

	def ox(self):
		hexstr = (hex(self.value))[2:].lower()
		return (('0x'+hexstr) if len(hexstr)&1 == 0 else ('0x0' + hexstr))

	#### static method, but for compatible with 2.6.6, use instance instead
		
	def get_hex(self, hexstr):
		return Hex(int(hexstr, 16))
		
	def get_list(self, bytes):
		return [str(Hex(byte)) for byte in bytes]

	def get_hex_list(self, bytes):
		return [repr(Hex(byte)) for byte in bytes]

	def get_int_bytes(self, bytes):
		return int.from_bytes(bytes, Hex.LITTLE)

	def get_big_int_bytes(self, bytes):
		return int.from_bytes(bytes, Hex.BIG)
	
	def set_int_bytes(self, value, length):
		return int.to_bytes(value, length, Hex.LITTLE)

	def get_offset(self, value, length):
		return [int(thebyte) for thebyte in int.to_bytes(value, length, Hex.LITTLE)]

	def get_hex_str(self, offset):
		return ''.join([str(Hex(thebyte)) for thebyte in offset])

	def get_binary(self, bytesstr):
		return bytearray([int(bytestr,16) for bytestr in bytesstr.strip().split(' ') if bytestr !=''])

class ServerCaller():
	''' Wrapper for IPMIToool '''
	def __init__(self, host, user, password):
		self._username = user
		self._hostname = host
		self._password = password
		self.Hex = Hex()

	def ipmicall_raw_call(self, rawparams):
		os.environ['IPMI_PASSWORD'] = self._password
		command = 'IPMITool -H {0} -U {1} -E -I lanplus '.format(self._hostname, self._username) + ' '.join(['raw'] + [repr(Hex(rawparam)) for rawparam in rawparams])
		debug(command + "\n")

		theprocess = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(stdout, stderr) = theprocess.communicate()
		errstr = stderr.decode('utf-8') 
		if errstr != '':
			# error(errstr + ' from ipmitool ' + ipmicommand)
			raise IPMIException(errstr + ' from ipmitool ' + ipmicommand)

		binary = self.Hex.get_binary(stdout.decode('utf-8'))

		return binary
		
	def ipmicall_raw_spawn(self, rawparams):
		os.environ['IPMI_PASSWORD'] = self._password
		command = 'IPMITool -H {0} -U {1} -E -I lanplus '.format(self._hostname, self._username) + ' '.join(['raw'] + [repr(Hex(rawparam)) for rawparam in rawparams])
		debug(command + "\n")
		theprocess = subprocess.Popen(shlex.split(command), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

		return theprocess

class BIOSFileSchemaParser:
	FILE_MARKS = ['ITM', 'OPT', 'STR', 'PRT']
	HEADER_SIZE = 32
	TIMESTAMP_SIZE = 4
	
	ONE_OF = 1
	CURRENT_VALUE = 2

	CONFIG_FORMATS = ['','''
[{VariableName}({QuestionId:08X})]
Prompt={PromptIdStr}
Option=''', '''
[{VariableName}({QuestionId:08X})]
Prompt={PromptIdStr}
MinValue={MinValue}
MaxValue={MaxValue}
DefaultValue={DefaultValue}
CurrentValue={CurrentValue}''', '''
[{VariableName}({QuestionId:08X})]
Prompt={PromptIdStr}
Option=''']
	
	def __init__(self):
		item_table_schema = [
				[ 4,'QuestionId', int],
				[ 2,'PromptId', int],
				[16,'VariableGuid', Hex],
				[50,'VariableName', str],
				[ 2,'VarOffset',Hex],
				[ 1,'VarSize', int],
				[ 1,'ValueType', int],
				[ 8,'CurrentValue', int],
				[ 8,'DefaultValue', int],
				[ 1,'OptionNumber', int],
				[ 2,'OptionStartOffset', int],
				[ 8,'MinValue', int], 
				[ 8,'MaxValue', int]]
		
		self.fileinfo = {
			BIOSFileSchemaParser.FILE_MARKS[0]: { # 'ITM'
				'Description': 'Item Table',
				'Schema': item_table_schema,
				'Parser': self.parse_item_table},
			BIOSFileSchemaParser.FILE_MARKS[1]: { # 'OPT'
				'Mark': BIOSFileSchemaParser.FILE_MARKS[1],
				'Description': 'Option Table',
				'Schema': [[ 2, 'StringId', Hex],[ 8, 'OptionValue', Hex]],
				'Parser': self.parse_option_table},
			BIOSFileSchemaParser.FILE_MARKS[2]: { # 'STR'
				'Mark': BIOSFileSchemaParser.FILE_MARKS[2], 
				'Description': 'String Table',
				'Schema': [[100, 'Name', str]],
				'Parser': self.parse_string_table},
			BIOSFileSchemaParser.FILE_MARKS[3]: { # 'PRT'
				'Mark': BIOSFileSchemaParser.FILE_MARKS[3],
				'Description': 'Partial Update Table',
				'Schema': [[ 4, 'QuestionId', int],[ 8, 'Value', int]],
				'Parser': self.parse_update_table}
			}
			
		# to compatible with 2.6.6
		self.Hex = Hex()

		self.fieldinfo = {}
		self._calculate_field_location()
		
	def _calculate_field_location(self):
		for filetype in self.fileinfo.keys():
			schema = self.fileinfo[filetype]['Schema']
			start = 0
			self.fieldinfo[filetype] = dict()
			for fieldinfo in schema:
				fieldinfo.append(start)
				self.fieldinfo[filetype][fieldinfo[1]] = fieldinfo
				start += fieldinfo[0]
				
			self.fileinfo[filetype]['RecordSize'] = start
			
		return

	## Parse binary to get field value
	def _get_field_length(self, filetype, fieldname):
		return self.fieldinfo[filetype][fieldname][1]
		
	def _get_binary_data(self, filetype, fieldname, binary):
		fieldinfo = self.fieldinfo[BIOSFileSchemaParser.FILE_MARKS[filetype]][fieldname]
		result = binary[fieldinfo[3]:fieldinfo[3] + fieldinfo[0]]
		return result

	def _get_binary_str(self, filetype, fieldname, binary):
		result = ''

		try:
			result = str(self._get_binary_data(filetype, fieldname, binary).decode('latin-1')).strip('\x00\x20')
		except ex:
			raise BinFileFormatException("Get string data failed {0} on '{1}'. {2}".format(fieldname, str(binary[0:8]), str(ex)))
			
		return result
		
	def _get_binary_int(self, filetype, fieldname, binary):
		result = 0
		
		try:
			result = self.Hex.get_int_bytes(self._get_binary_data(filetype, fieldname, binary))
		except Exception as ex:
			raise BinFileFormatException("Get integrate data failed {0} on '{1}'.  Message: {2}".format(fieldname, str(binary[0:8]), str(ex)))
			
		return result
		
	def _get_binary_hex(self, filetype, fieldname, binary):
		result = 0
		
		try:
			result = self.Hex.get_hex_str(self._get_binary_data(filetype, fieldname, binary))
		except Exception as ex:
			raise BinFileFormatException("Get hex data failed {0} on '{1}'.  The message: {2}".format(fieldname, str(binary[0:8]), str(ex)))
			
		return result
	
	def _get_data(self, filetype, fieldname, binary):
		result = 0
		fieldinfo = self.fieldinfo[BIOSFileSchemaParser.FILE_MARKS[filetype]][fieldname]

		if fieldinfo[2] == int:
			result = self._get_binary_int(filetype, fieldname, binary)
		elif fieldinfo[2] == str:
			result = self._get_binary_str(filetype, fieldname, binary)
		elif fieldinfo[2] == Hex:
			result = self._get_binary_hex(filetype, fieldname, binary)
		else:
			raise BinFileFormatException("Cannot determine type for {0} on data '{1}'".format(fieldname, str(binary[0:8])))
			
		return result
	
	## Parse Schema Record
	def _has_record(self, filetype, binary):
		recordsize = self.fileinfo[BIOSFileSchemaParser.FILE_MARKS[filetype]]['RecordSize']
		return (recordsize <= len(binary), recordsize)

	def _read_data(self, obj):
	
		binary = bytearray()
		pos = 0
		
		filemark = BIOSFileSchemaParser.FILE_MARKS[obj['FileType']]
		obj['FileHandle'].seek(BIOSFileSchemaParser.HEADER_SIZE)
		binary = obj['FileHandle'].read(obj['ChunkSize'])
		
		while True:
			(found, recordsize) = self._has_record(obj['FileType'], binary[pos:])
			while found:
				self.fileinfo[filemark]['Parser'](obj, binary[pos:])
				pos = pos + recordsize 
				(found, recordsize) = self._has_record(obj['FileType'], binary[pos:])

			binary = binary[pos:] + obj['FileHandle'].read(obj['ChunkSize'])
			
			# we want to skip the timestamp at the end of item table
			if len(binary) < 5: 
				obj['FileHandle'].close()
				pos = 0
				break
			elif pos == 0: # no record but it is at the end of file
				raise BinFileFormatException('Invalid FileFormat {0}'.format(obj['File']))
				break
				
			obj['Counter'] = obj['Counter'] + 1
			pos = 0

	def parse_string_table(self, obj, binary):
		namestr = self._get_binary_str(obj['FileType'], 'Name', binary)

		debug(str(len(obj['Data'])) + ':' + namestr)
		obj['Data'].append(namestr)
		
	def parse_option_table(self, obj, binary):
		strings = obj['Parent'][BIOSFileSchemaParser.FILE_MARKS[2]]['Data']
		filetype = obj['FileType']
		stringidint = self._get_binary_int(filetype, 'StringId', binary)
		optionvalueint = self._get_binary_int(filetype, 'OptionValue', binary)
		
		debug(str(len(obj['Data'])) + ':' + strings[stringidint] + ' = ' + str(optionvalueint))
		obj['Data'].append([strings[stringidint], optionvalueint])
		
	def parse_item_table(self, obj, binary):
		filetype = obj['FileType']
		itemid = obj['Counter']
		
		data = {}
		for fieldname in self.fieldinfo[BIOSFileSchemaParser.FILE_MARKS[filetype]].keys():
			try:
				data[fieldname] = self._get_data(filetype, fieldname, binary)
			except BinFileFormatException as ex:
				raise BinFileFormatException('Item table is invalid.  Message:'+ str(ex))

		try:
			valuetypeint = data['ValueType']
			
			strings = obj['Parent'][BIOSFileSchemaParser.FILE_MARKS[2]]['Data']
			options = obj['Parent'][BIOSFileSchemaParser.FILE_MARKS[1]]['Data']
			data['PromptIdStr'] = strings[data['PromptId']]
			
			sectiondata = ''
			if valuetypeint == 1: # One Of
				optionitems = []
				optionnum = data['OptionNumber']
				optionstart = data['OptionStartOffset']
				for optionid in range(optionstart, optionstart + optionnum):
					optionitems.append(
							'[{0}] {1} [{2}] {3}'.format(
							(' ' if options[optionid][1] != data['CurrentValue'] else 'X'),
							options[optionid][0],
							options[optionid][1],
							(' ' if options[optionid][1] != data['DefaultValue'] else '<default>')))
				sectiondata = (BIOSFileSchemaParser.CONFIG_FORMATS[valuetypeint].format(**data) + 
						'\n       '.join(optionitems)).replace("\r\n", "\n") + "\n\n"

			elif valuetypeint == 2: # Numeric
				sectiondata = BIOSFileSchemaParser.CONFIG_FORMATS[valuetypeint].format(**data).replace("\r\n", "\n") + "\n\n"

			elif valuetypeint == 3: # Checkbox
				booleanitems = []
				for booleanvalue in range(2):
					booleanitems.append(
							'[{0}] {1} [{2}] {3}'.format(
							(' ' if booleanvalue != data['CurrentValue'] else 'X'),
							['Disabled','Enabled'][booleanvalue],
							booleanvalue,
							(' ' if booleanvalue != data['DefaultValue'] else '<default>')))
				sectiondata = (BIOSFileSchemaParser.CONFIG_FORMATS[valuetypeint].format(**data) + 
						'\n       '.join(booleanitems)).replace("\r\n", "\n") + "\n\n"

			else:
				raise BinFileFormatException('Invalid data in {0}'.format(data['VariableGuid']))
				
			obj['Info']['{0:08X}'.format(data['QuestionId'])] = len(obj['Data'])
			obj['Data'].append(sectiondata)

		except BinFileFormatException as ex:
			raise BinFileFormatException('Parsing Item Table Field  Failed. ' + str(ex))
			raise ex
			
	def parse_update_table(self, obj, binary):
		''' parse update table '''
		questionidint = self._get_binary_int(obj['FileType'], 'QuestionId', binary)
		questionidstr = '({0:08X})'.format(questionidint)
		valueint = self._get_binary_int(obj['FileType'], 'Value', binary)
		
		obj['Data'].append([questionidstr, str(valueint), '['+str(valueint)+']'])
		
		
class HostBIOSAdapter:
	''' An adapter to operate BIOS read / modify through IPMI caller'''
	# related ipmitool raw command
	NET_FUNCTION=0x2E
	GET_BIOS_SETUP_STATUS=0xB0
	SET_BIOS_SETUP_DATA=0xB1
	GET_BIOS_SETUP_DATA=0xB2
	USER_SET_BIOS_SETUP_DATA=0xB3
	USER_GET_BIOS_SETUP_DATA=0xB4

	# job list's index
	JOB_PARAMS = 0
	JOB_HANDLE = 1
	JOB_STATUS = 2
	JOB_TRIALS = 3

	# can_skip; by check crc or check timestamp, both or None as 'check file exist only'
	BY_CRC = 1
	BY_TIMESTAMP = 2

	# host_info order
	VERSION = 0
	ITEMCHECKSUM = 1
	ITEMTIMESTAMP = 2
	UPDATETIMESTAMP = 3
	
	
	# record field sizes
	CHECKSUM_SIZE = 4
	TIMESTAMP_SIZE = 4
	HEADER_SIZE = 32
	BLOCK_SIZE = 16384 # [0x00, 0x40]
	STAMPEXT = '.timestamp'
	
	LOADING_SEQUENCE = [2, 1, 0, 3]

	# config header
	CONFIG_HEADER = '''
;;Do Not Modify This Section
# [BIOSSetup]
# Version={0}'''

	def __init__(self, caller, ip, updatecfg = ''):
		# self.TERMS = ['ITM','OPT','STR','PRT']
		
		self.ip = ip
		self.caller = caller
		
		self.binary = None
		self.config = None
		self.update = None
		self.previoussynced = False

		self.status = None
		self.version = None
		self.itemchecksum = None
		self.itemtimestamp = None
		self.updatetimestamp = None
		
		self.binfiles = [None] * len(BIOSFileSchemaParser.FILE_MARKS)
		self.schemaparser = BIOSFileSchemaParser()
		
		self.templateupdated = False
		self.tableloaded = False
		# self.loadedtable = {}
		
		# self.updatable = True
		# self.renames = []
		self.files = []
		self.updatecfg = updatecfg
		
		self.Hex = Hex()
	
	def __try_make_dir(self, dir):
		try:
			os.mkdir(dir)
		except Exception as ex:
			if not os.path.isdir(dir):
				raise ex
				
	def __try_remove(self, filespec):
		try:
			os.remove(filespec)
		except Exception as ex:
			if os.path.isfile(filespec):
				raise ex

	def __force_remove(self, file):
		while os.path.isfile(file):
			try:
				os.remove(file)
			except:
				debug('.')
				time.sleep(1)
				pass
			
	def _dump_job_hex(self, host, hexparams):
		return str(host) + ' => ' + ' '.join([str(Hex(item)) for item in hexparams])

	def _get_server_epoch_time_to_localtime(self, thebytes):
		return int.from_bytes(thebytes, 'big') - time.timezone # convert to local time
	
	def _get_time_epoch_bytes(self, thetime):
		return int.to_bytes(int(time.mktime(time.gmtime(thetime))), 4, 'big')
	
	def _collect_errors(self, errors, error):
		errors.append(error)
		
	def _validate_basic_header(self, source, header, filetype):
	
		errors = []
		filemark = header[0:5].decode('utf-8').strip('\x00')
		if filemark != '_FX_ ':
			self._collect_errors(errors, 'Invalid file mark {0}'.format(filemark))
			
		filetypestr = header[5:8].decode('utf-8').strip('\x00')
		if filetypestr != BIOSFileSchemaParser.FILE_MARKS[filetype]:
			self._collect_errors(errors, 'Invalid file type {0}'.format(filetypestr))
		
		headerver = header[8:24].decode('utf-8').strip('\x00')
		if headerver != self.version:
			self._collect_errors(errors, 'Invalid version {0}'.format(headerver))
		
		if len(errors) > 0:
			raise BinFileHeaderInvalidException('\n'.join(errors) + ' in {0}'.format(source))
		
		filesize = int.from_bytes(header[24:28], 'little')
		if not self._match_recordsize(filetype, filesize):
			raise BinFileHeaderInvalidException('File length of {0} is {1} not fit into records.'.format(source, str(filesize)))
		
		checksum = int.from_bytes(header[28:32], 'little')
		
		return (filesize, checksum) 

	def _check_server_crc(self, source, filetype, checksum):
		binary = self.caller.ipmicall_raw_call([self.NET_FUNCTION, self.GET_BIOS_SETUP_DATA, filetype]	+ self.Hex.get_offset(28, 4) + self.Hex.get_offset(self.CHECKSUM_SIZE, 2))
		serverchecksum = int.from_bytes(binary, 'little')
		self.previoussynced = (checksum == serverchecksum)

		if checksum != serverchecksum:
			info('The file {0} checksum is {1} different from server checksum is {2}'.format(
					source, 
					self.Hex.get_hex_str(self.Hex.get_offset(checksum, 4)), 
					self.Hex.get_hex_str(self.Hex.get_offset(serverchecksum, 4))))
		else:
			info('The server type={0} checksum is {1}'.format(filetype, self.Hex.get_hex_str(self.Hex.get_offset(serverchecksum, 4))))

		return self.previoussynced

	def _validate_value(self, settingtype, loadedtable, questionid, thevalue):
		result = False
		try:
			sectiondata = loadedtable['ITM']['Data'][loadedtable['ITM']['Info'][questionid]]
			if settingtype == BIOSFileSchemaParser.ONE_OF:
				checkvalue = '[' + str(thevalue) + ']'
				if sectiondata.find(checkvalue) >= 0:
					result = True
			elif settingtype == BIOSFileSchemaParser.CURRENT_VALUE:
				minvalue = int(re.search('MinValue=(\d+)', sectiondata)[1])
				maxvalue = int(re.search('MaxValue=(\d+)', sectiondata)[1])
				checkvalue = int(thevalue)
				if minvalue <= checkvalue <= maxvalue:
					result = True
			
		except Exception as ex:
			debug('Validate failed because {0}.'.format(ex))

		return result
		
	def _match_recordsize(self, filetype, filesize):
		# There is a 4 bytes timestamp at the bottom of PRT and ITM file.
		if BIOSFileSchemaParser.FILE_MARKS[filetype] in ['PRT', 'ITM']:
			# Avoid 0 byte situation.
			if filesize > HostBIOSAdapter.TIMESTAMP_SIZE:
				filesize = filesize - HostBIOSAdapter.TIMESTAMP_SIZE

		# Remainings should be fit into record size
		return filesize % self.schemaparser.fileinfo[BIOSFileSchemaParser.FILE_MARKS[filetype]]['RecordSize'] == 0
		
	def get_server_table_header(self, filetype, targetfile, targettemp, checkserver=False):
		header = None
		filesize = None
		checksum = None

		while True:
			# if one new one is creating, recheck again after that finish.
			if os.path.isfile(targettemp):
				debug("Try to wait temp can be removed\n")
				self.__force_remove(targettemp)
				continue
				
			# if checkserver: # as spec, we have to download update everytime
				# self.__force_remove(targetfile)
				# continue
				
			if os.path.isfile(targetfile):
				time.sleep(1)
				fh = open(targetfile, 'rb')
				header = fh.read(HostBIOSAdapter.HEADER_SIZE)
				fh.close()

				(filesize, checksum) = self._validate_basic_header(targetfile, header, filetype)
				validfile = (not checkserver) or self._check_server_crc(targetfile, filetype, checksum)

				# Valid target file.
				if validfile and (filesize == os.path.getsize(targetfile) - self.HEADER_SIZE):
					debug('{0} is valid. skip'.format(targetfile))
					return [True, header, filesize, checksum]

				# remove invalid file, recheck and/or create new one if possible.
				debug("Remove outdate file {0}\n".format(targetfile))
				self.__force_remove(targetfile)
				continue 

			# no one do, so we can call
			header = self.caller.ipmicall_raw_call([self.NET_FUNCTION, self.GET_BIOS_SETUP_DATA, filetype] + self.Hex.get_offset(0, 4) + self.Hex.get_offset(self.HEADER_SIZE, 2))
			(filesize, checksum) = self._validate_basic_header(self.ip, header, filetype)
			break
		
		return [False, header, filesize, checksum] 
		
	def _gen_config_header_text(self, version):
		headertext = HostBIOSAdapter.CONFIG_HEADER.format(version).strip().replace("\r\n", "\n") + "\n\n"
		return headertext
		
	# def can_update(self):
		# return self.updatable
		
	def can_skip(self, hostinfo, file, method=0):
		if not os.path.isfile(file):
			return False
			
		skipable = True
		if (method & HostBIOSAdapter.BY_CRC) != 0:
			fh = open(file, 'rb')
			binary = fh.read(self.HEADER_SIZE)
			fh.close()
			skipable = skipable and (binary[28:] == hostinfo[HostBIOSAdapter.ITEMCHECKSUM]) # hostinfo is 
		
		# check file
		if (method & HostBIOSAdapter.BY_TIMESTAMP) !=0:
			skipable = skipable and os.path.getmtime(file) == hostinfo[HostBIOSAdapter.UPDATETIMESTAMP] # self._get_server_epoch_time_to_localtime(validatecode)

		return skipable

	def check_time(self, *files):
		if not os.path.isfile(files[0]):
			return False
			
		basetime = int(os.path.getmtime(files[0]))
		for file in files[1:]:
			if not os.path.isfile(file):
				return False
			elif int(os.path.getmtime(file)) != basetime:
				return False
				
		return True
		
	def print_server_status(self, binary):
		info('''
-------------------------------------------
- Server: {0}
- Status: {1}
- BIOS Version: {2}
- Item Checksum: {3}
- Item Timestamp: {4}
- Update Timestamp: {5}
-------------------------------------------'''.format(
				self.ip, 
				int(binary[0]), 
				binary[1:17].decode('utf-8').strip('\x00'),
				self.Hex.get_hex_str(binary[17:21]),
				time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(self._get_server_epoch_time_to_localtime(binary[21:25]))),
				time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(self._get_server_epoch_time_to_localtime(binary[25:29]))))) 

	def check_related_files(self):
	
		verdir = os.path.abspath(os.path.join(os.path.curdir, self.version))
		if not os.path.isdir(verdir):
			self.__try_make_dir(verdir)
		
		os.environ['Host'] = self.ip
		os.environ['Version'] = self.version
		os.environ['ItemVersion'] = self.itemchecksum
		os.environ['Binary'] = self.binary = os.path.join(verdir, 'binary')
		os.environ['Config'] = self.config = os.path.join(verdir, 'config')
		os.environ['Update'] = self.update = os.path.join(verdir, 'update')

		for subdir in [self.binary, self.config, self.update]:
			self.__try_make_dir(subdir)

		self.files = [
			['STR_BIN', os.path.join(self.binary, 'string.bin')],
			['OPT_BIN', os.path.join(self.binary, 'option.bin')],
			['ITM_BIN', os.path.join(self.binary, 'item.${ItemVersion}.bin')],
			['PRT_BIN', os.path.join(self.binary, 'update.${ItemVersion}.${Host}.bin')],
			['CFG_ALL', os.path.join(self.config, 'template.${ItemVersion}.cfg')],
			['CFG_PRV', os.path.join(self.config, 'update.${ItemVersion}.${Host}.cfg')],
			['CFG_ADD', self.updatecfg],
			['CFG_CRC', self.updatecfg + '.crc'],
			['CFG_NEW', os.path.join(self.update, 'update.${Host}.cfg')],
			['BIN_NEW', os.path.join(self.update, 'update.${Host}.bin')]
		]
		
		for item in self.files:
			fileexist = ' '
			filestamp = ' ' * 19
			item[1] = re.subn('\$\{(\w+)\}', lambda x: os.environ[x.group(1)], item[1])[0]
			
			if os.path.isfile(item[1]):
				fileexist = 'X'
				filestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(os.path.getmtime(item[1])))
				
			info('- {0} : [{1}] [{2}] {3}'.format(item[0], fileexist, filestamp, item[1]))
			
		info('-------------------------------------------')
		self.files = dict(self.files)

	def load_template_config(self, templatecfg):
		tempmark = '!==!'
		loadeditemtable = dict()
		loadeditemtable['ITM'] = {'Data': list(), 'Info': dict()}
		fh = open(templatecfg)
		totallines = ''.join(fh.readlines())
		fh.close()
		
		loadeditemtable['ITM']['Data'] = re.subn('\[[^\]\(]+\(([^\)]+)\)\]', lambda x: (tempmark + x.group(0)),  totallines)[0].split(tempmark)
		for index in range(len(loadeditemtable['ITM']['Data'])):
			matched = re.search('\[[^\]\(]+\(([^\)]+)\)\]', loadeditemtable['ITM']['Data'][index])
			if matched:
				questionid = matched.group(1)
				loadeditemtable['ITM']['Info'][questionid] = index
		
		return loadeditemtable
		
	def check_update_crc(self, templatecfg, updatecfg, crcfile):
	
		targetfile = crcfile
		targettemp = targetfile + '.temp'
		
		fhcrc = None
		fhtemp = None
		while True:
			if os.path.isfile(targettemp):
				debug("Try to wait till the update file has completed DRC3checked d\n")
				time.sleep(1)
				self.__force_remove(targettemp)
				continue
			
			if os.path.isfile(targetfile):
				if not self.check_time(targetfile, updatecfg):
					time.sleep(1)
					if not self.check_time(targetfile, updatecfg):
						self.__force_remove(targetfile)
						continue

				# other has generated
				break
				# return os.path.isfile(targetfile)
			
			try:
				fhtemp = open(targettemp, 'w')
				
				loaded = True

				headertext = self._gen_config_header_text(self.version)
				loadeditemtable = self.load_template_config(templatecfg)
				self._parse_config(loadeditemtable, updatecfg, headertext, True)
				checksum=binascii.crc32(loadeditemtable['PRT']['Records'])
				
				fhcrc = open(targetfile, 'wb')
				fhcrc.write(int.to_bytes(checksum, 4, 'little'))
				fhcrc.close()
				
				timestamp = int(os.path.getmtime(updatecfg))
				os.utime(targetfile, (timestamp, timestamp))
				
				fhtemp.close()
				self.__force_remove(targettemp)

				# self.loadedtable = loadedtable
				
				# if template is updated, updateddate.cfg has to update always
				info('Update CRC {0} has verified.'.format(targetfile))
				break

			except Exception as ex:
				if fhcrc is not None:
					fhcrc.close()
					fhcrc = None
					
				if fhtemp is not None:
					fhtemp.close()
					fhtemp = None
				
				error('Write target file {0} failed. {1}'.format(targetfile, ex))
				
				time.sleep(2)
				
		return os.path.isfile(targetfile)
		
	def get_host_info(self):
		try:
			retries = 0
			while True:
				try:
					binary = self.caller.ipmicall_raw_call([
							self.NET_FUNCTION, 
							self.GET_BIOS_SETUP_STATUS])
					self.status = int(binary[0])
					self.version = binary[1:17].decode('utf-8').strip('\x00')
					
					# self.itemchecksum = int_from_bytes(binary[17:21], 'little') if len(binary) == 29 else 0
					self.itemchecksum = self.Hex.get_hex_str(binary[17:21]) # int_from_bytes(binary[17:21], 'little') if len(binary) == 29 else 0
					self.itemtimestamp = self._get_server_epoch_time_to_localtime(binary[21:25]) # it is useless from client
					self.updatetimestamp = self._get_server_epoch_time_to_localtime(binary[25:29])

					self.print_server_status(binary)
					
				except Exception as ex:
					if retries > 18:
						raise Exception('The host {0} is busy more than 180 seconds. {1}'.format(self.ip, str(ex)))
					retries = retries + 1				
					time.sleep(10)
		
				if self.status == 0:
					raise Exception('BIOS SETUP Status of {0} has no data'.format(self.ip))

				if self.status == 2:
					info('Server {0} is in CHANGED mode.'.format(self.ip))
					# self.updatable = False
				
				break
					
			if self.version is None:
				raise Exception('The host {0} cannot retrieve its version'.format(self.ip))

			self.check_related_files()
			
		except Exception as ex:
			error('Host version is invalid. ' + str(ex))
			raise ex
			
		return [self.version, self.itemchecksum, self.itemtimestamp, self.updatetimestamp]

	def change_bin_file(self, filetype, targetfile):
		self.binfiles[filetype] = targetfile

	def get_server_table(self, filetype, binfile, checkserver=False): # folder, fileprefix, fileext, checkserver=False):
		filesize = None
		checksum = None
		header = None
		
		# targettemp = os.path.join(folder, targetfilename + '.temp')
		targetfile = binfile
		targettemp = binfile + '.temp'
		
		self.change_bin_file(filetype, targetfile)
		
		(fileexist, header, filesize, checksum) = self.get_server_table_header(filetype, targetfile, targettemp, checkserver)
		
		if fileexist:
			return True
			
		fhtemp = None
		valid = False
		try:
			if os.path.isfile(targettemp):
				time.sleep(1) # someone is generate, wait
				raise BinFileExistException('Another is creating {0}'.format(targettemp))
				
			fhtemp = open(targettemp, 'wb')
			
			offset = self.HEADER_SIZE
			pages = int((filesize-1) / self.BLOCK_SIZE) + 1
			
			childjobs = []
			binaries = [None] * pages
			
			for page in range(pages):
				childjob = [
						[self.NET_FUNCTION, self.GET_BIOS_SETUP_DATA, filetype] + 
						self.Hex.get_offset(offset, 4) + 
						self.Hex.get_offset(self.BLOCK_SIZE, 2),
					    None, 
						None, 
						0]
				childjob[HostBIOSAdapter.JOB_HANDLE] = self.caller.ipmicall_raw_spawn(childjob[HostBIOSAdapter.JOB_PARAMS])
				childjobs.append(childjob)
				offset += self.BLOCK_SIZE

			needwait = True
			
			while needwait:
				needwait = False
				for childjob in childjobs:
					if childjob[HostBIOSAdapter.JOB_STATUS] is not None:
						debug("Skip because {0} is loaded\n".format(self.Hex.get_hex_str(childjob[HostBIOSAdapter.JOB_PARAMS][3:7])))
						continue
						
					(stdout, stderr) = childjob[HostBIOSAdapter.JOB_HANDLE].communicate()
					if stderr != b'':
						if childjob[HostBIOSAdapter.JOB_TRIALS] >=2:
							raise IPMIException('Cannot retrieve segment {0} of {1} correctly'.format(self.Hex.get_hex_str(childjob[HostBIOSAdapter.JOB_PARAMS][3:7]), targetfile))
							
						childjob[HostBIOSAdapter.JOB_HANDLE] = self.caller.ipmicall_raw_spawn(childjob[HostBIOSAdapter.JOB_PARAMS])
						childjob[HostBIOSAdapter.JOB_TRIALS] = childjob[HostBIOSAdapter.JOB_TRIALS] + 1
						needwait = True

						debug("Reschedule {0} because has error {1}\n".format(self.Hex.get_hex_str(childjob[HostBIOSAdapter.JOB_PARAMS][3:7]), stderr.decode('utf-8')))
						continue
					
					childjob[HostBIOSAdapter.JOB_STATUS] = self.Hex.get_binary(stdout.decode('utf-8'))
			
			fh = open(targetfile, 'w+b')
			fh.write(header)
			
			checkbin = 0
			for childjob in childjobs:
				checkbin = binascii.crc32(childjob[HostBIOSAdapter.JOB_STATUS], checkbin)
				fh.write(childjob[HostBIOSAdapter.JOB_STATUS])
			
			fh.close()
			
			if checkbin != checksum:
				raise ImportError('Checksum for {0} is invalid'.format(targetfile))
		
			# fhtemp.close()
			# self.__force_remove(targettemp)
			
			info('{0} is created for {1}'.format(targetfile, self.ip))
			valid = True
		
		finally:#  Exception as ex:
			if fhtemp is not None:
				fhtemp.close()
			self.__force_remove(targettemp)

		return valid
		
	def _load_table(self, loadedtable, filetype):
		loadedtable[BIOSFileSchemaParser.FILE_MARKS[filetype]] = { 
				'File': self.binfiles[filetype], # for print message purpose
				'Parent': loadedtable,
				'FileType': filetype, 
				'Counter': 0, 
				'ChunkSize': self.BLOCK_SIZE, 
				'FileLength': os.path.getsize(self.binfiles[filetype]), 
				'FileHandle': open(self.binfiles[filetype],'rb'), 
				'Data': [],
				'Info': {}
				}
				
		self.schemaparser._read_data(loadedtable[BIOSFileSchemaParser.FILE_MARKS[filetype]])

	def generate_update_config(self, loadedtable, configfile, stamptime): # configfile, stamptime): #folder, fileprefix, fileext): #(self, loadedtable, folder, fileprefix, fileext):
		targetfile = configfile # os.path.join(folder, targetfilename)
		targettemp = configfile + '.temp'
		
		headertext = self._gen_config_header_text(self.version)
		headerlength = len(headertext)
		emptyheadertext = ' ' * (headerlength + 2)
		
		fhtemp = None
		fhconfig = None
		result = False
		
		while True:
			if os.path.isfile(targettemp):
				debug("Try to wait temp can be removed\n")
				self.__force_remove(targettemp)
				continue
			
			if os.path.isfile(targetfile):
				if not self.previoussynced:
					self.__force_remove(targetfile)
					continue
					
				if self.templateupdated:
					self.__force_remove(targetfile)
					continue
					
				time.sleep(2)
				
				filesize = os.path.getsize(targetfile)
				if filesize < headerlength:
					self.__force_remove(targetfile)
					continue
					
				fh = open(targetfile, 'rt')
				headerread = fh.read(headerlength)
				fh.close()
				if headerread != headertext:
					self.__force_remove(targetfile)
					continue

				# other has generated
				info('Valid {0} already exist.'.format(targetfile))
				return True
			
			try:
				fhtemp = open(targettemp, 'w')

				if not self.tableloaded:
					# 2,1,0,3 is the correct sequence of filemark (type of files) to parse correct data
					# 2 - string table
					# 1 - option table
					# 0 - item table
					# 3 - update table
					loaded = True

					for filetype in HostBIOSAdapter.LOADING_SEQUENCE: # [2, 1, 0]: # 3]:
						try:
							self._load_table(loadedtable, filetype)
						except Exception as ex:
							if filetype != 3:
								error('Load table failed. ' + ex)
								loaded = False

					self.tableloaded = loaded
				
				fhconfig = open(targetfile, 'w+t', encoding='UTF-8')
				fhconfig.write(emptyheadertext)
				
				# Performance concern, so we collect update configuration here.
				output = []
				errors = []
				for item in loadedtable['ITM']['Data']:
					for upd in loadedtable['PRT']['Data']:
						# This assumes questionid is unique
						# upd[0] is questionid, upd[1] is  the value
						if item.find(upd[0]) >= 0: 
							pos = item.find('[X]  ')
							if pos >= 0: # one of or boolean
								item[pos+1] = ' ' # remove 'X' with ' '
								valuepos = item.index(upd[2])
								# mark the value item as 'X', throw 
								valuepos = item.rfind(']', 0, valuepos)
								if valuepos > 0:
									item[valuepos-1] = 'X'
								else:
									self._collect_errors(errors, 'Cannot find {0} value in {1} for host {2}'.format(
											upd[1], upd[0], self.ip))
							else: # 
								item = re.sub('CurrentValue=\d+', 'CurrentValue='+upd[1], item)
								
							output.append(item)
							
				if len(errors) > 0:
					raise Exception('\n'.join(errors) + ' in {0}'.format(prevupdateconfig))
				
				fhconfig.write(''.join(output))
				
				fhconfig.seek(0,0)
				fhconfig.write(headertext)
				fhconfig.close()
				
				os.utime(configfile, (stamptime, stamptime))
				
				result = True

			except Exception as exfs:
				error('Generate update.conf failed. ' + str(exfs))
				time.sleep(2)

			finally:
				if fhconfig is not None:
					fhconfig.close()
					fhconfig = None

				if fhtemp is not None:
					fhtemp.close()
					fhtemp = None
					self.__force_remove(targettemp)

			return result 
	
	def generate_template_config(self, loadedtable): # , folder, fileprefix, fileext):
		# targetfilename = fileprefix + fileext
		# targetfile = os.path.join(folder, targetfilename)
		# targettemp = os.path.join(folder, targetfilename + '.temp')
		
		targetfile = self.files['CFG_ALL']
		targettemp = targetfile + '.temp'
		
		headertext = self._gen_config_header_text(self.version)
		headerlength = len(headertext)
		emptyheadertext = ' ' * (headerlength+2)
		
		fhtemp = None
		fhconfig = None
		
		while True:
			if os.path.isfile(targettemp):
				debug("Try to wait temp can be removed\n")
				time.sleep(1)
				self.__force_remove(targettemp)
				continue
			
			if os.path.isfile(targetfile):
				time.sleep(2)
				filesize = os.path.getsize(targetfile)
				if filesize < headerlength:
					self.__force_remove(targetfile)
					continue
					
				fh = open(targetfile, 'rt')
				headerread = fh.read(headerlength)
				fh.close()
				if headerread != headertext:
					self.__force_remove(targetfile)
					continue

				# other has generated
				break
				# return os.path.isfile(targetfile)
			
			try:
				fhtemp = open(targettemp, 'w')
				
				loaded = True
				for filetype in HostBIOSAdapter.LOADING_SEQUENCE: # [2, 1, 0, 3]:
					try:
						self._load_table(loadedtable, filetype)
					except Exception as ex:
						if filetype != 3:
							error('Load table type={0} failed. {1}'.format(filetype, ex))
							loaded = False
						
				self.tableloaded = loaded

				if not self.tableloaded:
					return False

				fhconfig = open(targetfile, 'w+t', encoding='UTF-8')
				fhconfig.write(emptyheadertext)
				fhconfig.write(''.join(loadedtable['ITM']['Data']))
				fhconfig.seek(0,0)
				fhconfig.write(headertext)
				fhconfig.close()
				
				fhtemp.close()
				self.__force_remove(targettemp)

				self.templateupdated = True
				
				# self.loadedtable = loadedtable
				
				# if template is updated, updateddate.cfg has to update always
				info('Template config file {0} is generated.'.format(targetfile))

			except Exception as exfs:
				if fhconfig is not None:
					fhconfig.close()
					fhconfig = None
					
				if fhtemp is not None:
					fhtemp.close()
					fhtemp = None
				
				error('Write target file {0} failed. {1}'.format(targetfile, exfs))
				
				time.sleep(2)
				
		return os.path.isfile(targetfile)

	def _parse_config(self, loadedtable, configfile, headertext, validate=False):
		if not os.path.isfile(configfile):
			return False
			
		if 'PRT' not in loadedtable:
			loadedtable['PRT'] = {'Records': bytearray(), 'Info': dict()}
			
		obj = loadedtable['PRT']
		headerlength = len(headertext)

		fhconfig = open(configfile, 'rt', encoding='utf-8')
		header = fhconfig.read(headerlength*2)
		if header.find(headertext)==-1:
			fhconfig.close()
			raise Exception('Invalid config file {0}'.format(configfile))
		
		fhconfig.seek(0, 0)

		hasupdate = False
		errors = []
		# binary = bytearray()
		# checksum = 0
		for theline in fhconfig.readlines():
			matched = re.search('^\[\w+\(([0-9A-F]+)\)\]$', theline)
			if matched:
				QuestionId = matched.group(1)
				questionidbytes = int.to_bytes(self.Hex.get_hex(QuestionId), 4, 'little')
				continue
				
			matched = re.search('\[\S\]\s+[^\[]+\[(\d+)\]', theline)
			if matched: # valuetype=1 or 3
				thevalue = matched.group(1)
				
				# validate
				if validate and not self._validate_value(
						BIOSFileSchemaParser.ONE_OF, 
						loadedtable, 
						QuestionId, 
						thevalue):
					self._collect_errors(errors, 'The Section {0} and line {1} is out of range based on original template'.format(QuestionId, theline))
					continue
				
				valuebytes = int.to_bytes(matched.group(1), 8, 'little')
				chunk = questionidbytes + valuebytes
				if questionidbytes not in obj['Info']:
					pos = len(obj['Records'])
					obj['Info'][questionidbytes] = [pos,valuebytes]
					obj['Records'].extend(chunk)
					if not hasupdate:
						hasupdate = True
				elif valuebytes != obj['Info'][questionidbytes][1]:
					pos = obj['Info'][questionidbytes][0]
					obj['Info'][questionidbytes][1] = valuebytes
					obj['Records'][pos:pos+len(chunk)] = chunk
					if not hasupdate:
						hasupdate = True
				# if questionidbytes not in obj['info']:
					# pos = len(obj['records'])
					# obj['info'][questionidbytes] = [pos,valuebytes]
					# obj['records'].extend(chunk)
					# if not hasupdate:
						# hasupdate = True
				# elif valuebytes != obj['info'][questionidbytes][1]:
					# pos = obj['info'][questionidbytes][0]
					# obj['info'][questionidbytes][1] = valuebytes
					# obj['records'][pos:pos+len(chunk)] = chunk
					# if not hasupdate:
						# hasupdate = True
				
				# checksum = binascii.crc32(chunk, checksum)
				# binary.extend(questionidbytes + valuebytes)
				continue
				
			matched = re.search('CurrentValue=(\d+)', theline)
			if matched: # valuetype=2
				thevalue = matched.group(1)
				
				if validate and not self._validate_value(
						BIOSFileSchemaParser.CURRENT_VALUE, 
						loadedtable, 
						QuestionId, 
						thevalue):
					self._collect_errors(errors, 'The Section {0} and the line {1} is out of range based on original template'.format(QuestionId, theline))
					continue
					
				valuebytes = int.to_bytes(int(matched.group(1)), 8, 'little')
				chunk = questionidbytes + valuebytes
				if questionidbytes not in obj['Info']:
					pos = len(obj['Records'])
					obj['Info'][questionidbytes] = [pos,valuebytes]
					obj['Records'].extend(chunk)
					if not hasupdate:
						hasupdate = True
				elif valuebytes != obj['Info'][questionidbytes][1]:
					pos = obj['Info'][questionidbytes][0]
					obj['Info'][questionidbytes] = valuebytes
					obj['Records'][pos:pos+len(chunk)] = chunk
					if not hasupdate:
						hasupdate = True
				# if questionidbytes not in obj['info']:
					# pos = len(obj['records'])
					# obj['info'][questionidbytes] = [pos,valuebytes]
					# obj['records'].extend(chunk)
					# if not hasupdate:
						# hasupdate = True
				# elif valuebytes != obj['info'][questionidbytes][1]:
					# pos = obj['info'][questionidbytes][0]
					# obj['info'][questionidbytes] = valuebytes
					# obj['records'][pos:pos+len(chunk)] = chunk
					# if not hasupdate:
						# hasupdate = True

				# checksum = binascii.crc32(chunk, checksum)
				# binary.extend(questionidbytes + valuebytes)
				continue
		
		if len(errors) > 0:
			raise CFGFileException('\n'.join(errors) + ' in {0}'.format(configfile))

		fhconfig.close()
		return hasupdate

	def generate_update_bin(self, loadedtable, configfiles, updatebin, timestamp, forcesubmit = False):
		readyupdate = True
		
		targetfile = updatebin
		targettemp = updatebin + '.temp'
		
		headertext = self._gen_config_header_text(self.version)

		# obj = {'records': bytearray(), 'info':dict()}
		obj = loadedtable['PRT'] = {'Records': bytearray(), 'Info':dict()}
		
		fhtarget = None
		fhtargettemp = None
		
		try:
			fhtargettemp = open(targettemp, 'wb')
			
			# fhtargettemp.close()
			

			fileindex = 0
			if not forcesubmit:
				self._parse_config(loadedtable, configfiles[0], headertext)
				fileindex = 1

			noupdate = True
			for configfile in configfiles[fileindex:]:
				if self._parse_config(loadedtable, configfile, headertext):
					noupdate = False
					
				# if noupdate:
					# self.renames.append(configfile)

			# since hostupdateconfig has included all and it is the latest updated config in the process,
			# skip update bin and/or submit to the server
			if noupdate:
				fhtargettemp.close()
				return False
				
			self.updatetime = int(timestamp)
			obj['Records'].extend(self._get_time_epoch_bytes(self.updatetime))
					
			checksum=binascii.crc32(obj['Records'])
			datasize = len(obj['Records'])
			# pages = int((datasize-1)/self.BLOCK_SIZE) # skip + 1 as it is the last one which needs special calculate
			header = '_FX_ PRT'.encode() + self.version.ljust(16, '\x00').encode() + int.to_bytes(datasize, 4, 'little') + int.to_bytes(checksum, 4, 'little')
					
			fhtarget = open(updatebin, 'wb')
			
			fhtarget.write(header + obj['Records'])
			
			fhtarget.close()
			os.utime(updatebin, (int(self.updatetime), int(self.updatetime)))

			fhtargettemp.close()
			
		except Exception as ex:
			error('Generate update.bin ({0}) failed. {1}'.format(targetfile, str(ex)))
				
			readyupdate = False

		finally:			
			if fhtarget is not None:
				fhtarget.close()
				fhtarget = None

			if fhtargettemp is not None:
				fhtargettemp.close()
				fhtargettemp = None
				self.__force_remove(targettemp)

		return readyupdate
	
	def submit_update_bin(self, updatebin): #folder, targetfile):
	
		success = True
		try:
			fhtarget = open(updatebin, 'rb')
			header = fhtarget.read(self.HEADER_SIZE)
			binary = fhtarget.read(os.path.getsize(updatebin)-self.HEADER_SIZE)
			fhtarget.close()
			
			datasize = len(binary)
			pages = int((datasize-1)/self.BLOCK_SIZE) # skip + 1 as it is the last one which needs special calculate
			
			firstjob = [self.NET_FUNCTION, self.SET_BIOS_SETUP_DATA] + self.Hex.get_offset(0, 4) + self.Hex.get_offset(self.HEADER_SIZE, 2) + [int(thebyte) for thebyte in header]

			self.caller.ipmicall_raw_call(firstjob)
			debug('FIRSTJOB:' + self._dump_job_hex(self.ip, firstjob) + "\n")

			childjobs = []
			
			start = self.HEADER_SIZE
			for page in range(pages):

				childjob = [
						[self.NET_FUNCTION, self.SET_BIOS_SETUP_DATA] + 
						self.Hex.get_offset(start, 4) + 
						self.Hex.get_offset(self.BLOCK_SIZE, 2) + 
						self.Hex.get_hex_list(binary[page*self.BLOCK_SIZE:(page+1)*self.BLOCK_SIZE]),
						None, 
						None, 
						0]
				childjob[HostBIOSAdapter.JOB_HANDLE] = self.caller.ipmicall_raw_spawn(childjob[HostBIOSAdapter.JOB_PARAMS])
				debug('JOB {0}:'.format(page) + self._dump_job_hex(self.ip, childjob[HostBIOSAdapter.JOB_PARAMS]) + "\n")
				
				childjobs.append(childjob)

				start = start + self.BLOCK_SIZE
				
			lastjob = [self.NET_FUNCTION, self.SET_BIOS_SETUP_DATA] + self.Hex.get_offset(start, 4) + self.Hex.get_offset(datasize + self.HEADER_SIZE - start, 2) + [int(thebyte) for thebyte in binary[pages*self.BLOCK_SIZE:]]
			
			needwait = True
				
			while needwait:

				needwait = False

				for childjob in childjobs:
					if childjob[HostBIOSAdapter.JOB_STATUS] is not None:
						debug("Skip because {0} is loaded\n".format(self.Hex.get_hex_str(childjob[HostBIOSAdapter.JOB_PARAMS][3:7])))
						continue
						
					(stdout, stderr) = childjob[HostBIOSAdapter.JOB_HANDLE].communicate()
					if stderr != b'':
						if childjob[HostBIOSAdapter.JOB_TRIALS] >=2:
							raise BinFileSubmitException('Cannot retrieve segment {0} of {1} correctly'.format(self.Hex.get_hex_str(childjob[HostBIOSAdapter.JOB_PARAMS][3:7]), updatebin))
							
						info(self._dump_job_hex(childjob[HostBIOSAdapter.JOB_PARAMS]))
						
						childjob[HostBIOSAdapter.JOB_TRIALS] = childjob[HostBIOSAdapter.JOB_TRIALS] + 1
						needwait = True

						debug("Reschedule {0} because has error {1}\n".format(self.Hex.get_hex_str(childjob[HostBIOSAdapter.JOB_PARAMS][3:7]), stderr.decode('utf-8')))
						continue
					
					childjob[HostBIOSAdapter.JOB_STATUS] = stdout.decode('utf-8')
			
			self.caller.ipmicall_raw_call(lastjob)
			debug('LASTJOB: ' + self._dump_job_hex(self.ip, lastjob) + "\n")
			
			print('{0} has updated to {1}'.format(updatebin, self.ip))

			success = True

		except Exception as ex:
			error(ex)

		return success
		
	# def _move_config_to_backup(self, loadedtable, bintime):
		# # adapter.generate_update_config(loadedtable, hostconfig, hostinfo[3])
		# self.generate_update_config(loadedtable, self.files['CFG_NEW'], bintime) # updateobj, bintime)
		
		# for file in self.renames:
			# try:
				# os.rename(file, file + '.bak')
			# except:
				# pass
				
class BiosConfig:

	def __init__(self, statusonly=False, forcesubmit=False, forcelocalupdate=False):
		self.caller = None
		self.statusonly = statusonly
		self.forcesubmit = forcesubmit
		self.forcelocalupdate = forcelocalupdate
		
	def prepare(self, adapter, host, hostinfo, loadedtable):
		# record: recordtype, folder, filename, fileext, checkserver as same order as get_server_table
		
		# LOADING_SEQUENCE: 2, 1, 0, 3 (File Type)
		jobs = [[2, adapter.files['STR_BIN'], False], 
				[1, adapter.files['OPT_BIN'], False],
				[0, adapter.files['ITM_BIN'], True],
				[3, adapter.files['PRT_BIN'], True]]
				
		# check B0's item CRC. return True if no change
		if adapter.can_skip(hostinfo, adapter.files['ITM_BIN'], True):
			return True
			
		valid = True
		hasupdate = True

		# first time to ensure we do what we need to do, skip if other is running
		for job in jobs:
			notdone = True
			while notdone:
				try:
					adapter.get_server_table(*job)
					notdone = False
				except BinFileExistException as existerr:
					debug(str(existerr))
					notdone = True # retry
					pass
				except IPMIException as ipmierr:
					error('Get {0}.bin failed as IPMI command issue. {1}'.format(job[2], str(ipmierr)))
					valid = False
					notdone = False
				except ImportError as imperr:
					error('Get {0}.bin failed. {1}'.format(job[2], str(imperr)))
					valid = False
					notdone = False
				except Exception as ex:
					if job[0] != 3:					
						error('Get {0}.bin failed unexpect. {1}'.format(job[2], str(ex)))
						valid = False
					else:
						hasupdate = False

					notdone = False
		
		if not valid:
			return valid

		info('All bin files for host {0} is ready.'.format(adapter.ip))

		valid = adapter.generate_template_config(loadedtable) # , adapter.config, 'template', '.cfg')

		# (self, loadedtable, updateobj, hostupdateconfig, bintime): #folder, fileprefix, fileext): #(self, loadedtable, folder, fileprefix, fileext):

		# hostupdateconfig = os.path.join(adapter.config, 'update_' + host + '.cfg')

		valid = valid and hasupdate and adapter.generate_update_config(
				loadedtable, 
				adapter.files['CFG_PRV'],
				hostinfo[HostBIOSAdapter.UPDATETIMESTAMP])

		return valid 

	def submit(self, adapter, host, hostinfo, loadedtable):
		# suppose, can be removed as loading previous update config from server is no longer support.
		# keep as it is because no harm
		# prevupdateconfig = os.path.join(adapter.config, 'update_' + host + '.cfg')
		
		# adapter.hostupdateconfig = os.path.join(adapter.update, 'update_' + host + '.cfg')
		# hostupdateconfig = os.path.join(adapter.config, 'update_' + host + '.cfg')
		
		# updateconfig = os.path.join(adapter.config, 'update.cfg')
		# mergedupdateconfig = os.path.join(adapter.update, 'update_' + host + '.cfg')
		

		# updatebinfile = 'update_' + host + '.bin'
		# updatebin = os.path.join(adapter.update, updatebinfile)
		adapter.change_bin_file(3, adapter.files['BIN_NEW'])
		
		if self.forcesubmit:
			self.forcelocalupdate = False
		
		# If the server's time stamp is the same as local bin, skip
		if not self.forcelocalupdate and \
				not self.forcesubmit and \
				adapter.check_time(adapter.files['BIN_NEW'], adapter.files['CFG_ADD']) and \
				adapter.can_skip(hostinfo[HostBIOSAdapter.UPDATETIMESTAMP], adapter.files['BIN_NEW'], False):
			info('No update for Item table')
			return
			
		if not adapter.check_update_crc(adapter.files['CFG_ALL'], adapter.files['CFG_ADD'], adapter.files['CFG_CRC']):
			return
		
		readyupdate = adapter.generate_update_bin(
				loadedtable, 
				[adapter.files['CFG_PRV'], adapter.files['CFG_ADD'], adapter.files['CFG_NEW']],
				adapter.files['BIN_NEW'],
				int(os.path.getmtime(adapter.files['CFG_ADD'])),
				self.forcesubmit)

		if not readyupdate:
			info('No update bin {0} can be generated'.format(adapter.files['BIN_NEW']))
			if not self.forcesubmit:
				info('No update necessary.  Exit')
				return
			if os.path.getsize(adapter.files['BIN_NEW']) == 0:
				info('No update bin {0} generated.  Exit'.format(adapter.files['BIN_NEW']))
				return
		
		# if the host is updating, 
		# if not adapter.can_update() and not self.forcesubmit:
			# info('The server is updating by others.')
			# return
		
		if not self.forcelocalupdate and not adapter.submit_update_bin(adapter.files['BIN_NEW']):
			info('Submit to server failed.  Please rerun to resubmit')
			return

		timestamp = int(os.path.getmtime(adapter.files['BIN_NEW']))
		info('Updated bin has submitted to {0}'.format(adapter.ip))

		adapter.generate_update_config(loadedtable, adapter.files['CFG_NEW'], timestamp)

	def process(self, host, user, password, updatecfg=''):
		loadedtable = {}

		# wrapper to ipmitool
		self.caller = ServerCaller(host, user, password)

		# prepare the adapter to the server
		adapter = HostBIOSAdapter(self.caller, host, updatecfg)
		hostinfo = adapter.get_host_info()

		if self.statusonly:
			return
	
		if not self.prepare(adapter, host, hostinfo, loadedtable):
			info('Preparing template or server update config file have error(s).  Stop.')
			
		self.submit(adapter, host, hostinfo, loadedtable)


def main():
	def usage():
		print('BiosConfig -H <host> -U <user> -P <password> [-F <update>] [--statusonly] [--forcesubmit] [--forcelocalupdate]')

	syntax = {
		'-H':[str, '', '', ''],
		'-U':[str, '', '', ''],
		'-P':[str, '', '', ''],
		'-F':[str, '', '', ''],
		'--statusonly':[bool, False, False, None],
		'--forcesubmit':[bool, False, False, None],
		'--forcelocalupdate':[bool, False, False, None],
		'USAGE': usage,
		'ARGLIST': []
	}

	bc = None

	parseargs(syntax, sys.argv)
	bc = BiosConfig(
			syntax['--statusonly'][1],
			syntax['--forcesubmit'][1], 
			syntax['--forcelocalupdate'][1])
			
	bc.process(
			syntax['-H'][1],
			syntax['-U'][1],
			syntax['-P'][1],
			syntax['-F'][1])	

if __name__ == '__main__':
	main()
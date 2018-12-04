import sys,re,os,json,datetime,subprocess,shlex

# print(sys.argv[1])

mcinforesult = sys.argv[1]
(ipmicmd1, ipmicmd2, server_id, insert_time_filename, ext) = re.split(r'[\_\.]', os.path.basename(mcinforesult))
insert_time_mtime = os.path.getmtime(mcinforesult) if os.path.isfile(mcinforesult) else datetime.datetime.strptime(insert_time_filename, '%Y%m%d%H%M%S').timestamp()

ipmicmd = ipmicmd1 + ' ' + ipmicmd2
insert_time_basetime = datetime.datetime.strptime(insert_time_filename, '%Y%m%d%H%M%S')
insert_time_finishtime = datetime.datetime.fromtimestamp(insert_time_mtime)
insert_time = (insert_time_basetime + (insert_time_finishtime - insert_time_basetime) / 2).strftime('%Y%m%d%H%M%S')

mcinfodict={}
if os.path.isfile(mcinforesult):
	fh = open(mcinforesult)
	lines = fh.readlines()
	fh.close()

	for line in lines:
		kv = line.split(':')
		if len(kv)>=2:
			thekey = kv[0].strip()
			thevalue = ':'.join(kv[1:]).strip()
			if thevalue == '':
				subkey = thekey
				mcinfodict[thekey]=[]
			else:
				mcinfodict[thekey]=thevalue
		else:
			mcinfodict[subkey].append(line.strip())
		
isVerbose = '_VERBOSE' in os.environ
isTry = '_TRY' in os.environ

sqlfile = mcinforesult + '.sql'

fhsql = open(sqlfile, 'w+')

fhsql.write('use server_management;\n')

smt = {
	'insert_time': insert_time,
	'server_id': server_id,
	'json': json.dumps({ipmicmd:[mcinfodict]})
}

sqlsmt = "call insert_server_mc_info_json('{insert_time}', '{server_id}', '{json}');\n".format(**smt)

fhsql.write(sqlsmt)
		
fhsql.close()
	
obj = {
	'MYSQL': os.environ['MYSQL'],
	'DBUSER': os.environ['DBUSER'],
	'DBPWD': os.environ['DBPWD'],
	'SQLFILE': sqlfile
}

sqlcmd = '"{MYSQL}" -u{DBUSER} -p{DBPWD} < {SQLFILE}'.format(**obj)
if isVerbose:
	print(sqlcmd)

if not isTry:
	cmdline = shlex.split(sqlcmd, posix=False)
	cmdline[0] = cmdline[0].strip('"')
	cmdline[4] = cmdline[4].strip('"')
	lines = [line.strip().decode('utf-8') for line in subprocess.Popen(cmdline, shell=True, stderr=subprocess.PIPE).stderr.readlines()]
	errors = '\n'.join([line for line in lines if line.find('[Warning]')==-1])
	if errors != '':
		print(errors)

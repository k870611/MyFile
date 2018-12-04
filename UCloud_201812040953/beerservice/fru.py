import sys,re,os,json,datetime,subprocess,shlex

# print(sys.argv[1])

fruresult = sys.argv[1]
(ipmicmd, server_id, insert_time_filename, ext) = re.split(r'[\_\.]', os.path.basename(fruresult))
insert_time_mtime = os.path.getmtime(fruresult) if os.path.isfile(fruresult) else datetime.datetime.strptime(insert_time_filename, '%Y%m%d%H%M%S').timestamp()

insert_time_basetime = datetime.datetime.strptime(insert_time_filename, '%Y%m%d%H%M%S')
insert_time_finishtime = datetime.datetime.fromtimestamp(insert_time_mtime)
insert_time = (insert_time_basetime + (insert_time_finishtime - insert_time_basetime) / 2).strftime('%Y%m%d%H%M%S')

frudict={}
if os.path.isfile(fruresult):
	fh = open(fruresult)
	lines = fh.readlines()
	fh.close()

	for line in lines:
		kv = line.split(':')
		if len(kv)>=2:
			frudict[kv[0].strip()] = ''.join(kv[1:]).strip()

isVerbose = '_VERBOSE' in os.environ
isTry = '_TRY' in os.environ

sqlfile = fruresult + '.sql'

fhsql = open(sqlfile, 'w+')

fhsql.write('use server_management;\n')

smt = {
	'insert_time': insert_time,
	'server_id': server_id,
	'json': json.dumps({ipmicmd:[frudict]})
}

sqlsmt = "call insert_server_fru_json('{insert_time}', '{server_id}', '{json}');\n".format(**smt)

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

	
	
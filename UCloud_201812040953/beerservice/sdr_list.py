import sys,re,os,json,datetime,subprocess,shlex

# print(sys.argv[1])

sdrlistresult = sys.argv[1]
(ipmicmd1, ipmicmd2, server_id, insert_time_filename, ext) = re.split(r'[\_\.]', os.path.basename(sdrlistresult))
insert_time_mtime = os.path.getmtime(sdrlistresult) if os.path.isfile(sdrlistresult) else datetime.datetime.strptime(insert_time_filename, '%Y%m%d%H%M%S').timestamp()

ipmicmd = ipmicmd1 + ' ' + ipmicmd2
insert_time_basetime = datetime.datetime.strptime(insert_time_filename, '%Y%m%d%H%M%S')
insert_time_finishtime = datetime.datetime.fromtimestamp(insert_time_mtime)
insert_time = (insert_time_basetime + (insert_time_finishtime - insert_time_basetime) / 2).strftime('%Y%m%d%H%M%S')

sdrlistsubkey=['name', 'value', 'status', 'purevalue', 'unit']

sdrlistarray=[]
if os.path.isfile(sdrlistresult):
	fh = open(sdrlistresult)
	lines = fh.readlines()
	fh.close()

	for line in lines:
		items = [item.strip() for item in line.split('|')]
		values = items[1].split(' ')
		items.extend([values[0], ' '.join(values[1:])])
		if items[3].startswith('0x'):
			items[3] = str(int(items[3], 16))
		elif items[3] == 'no':
			items[3] = -1 # no reading
		elif items[3] == 'Not':
			items[3] = -2 # Not readable
			
		sdrlistarray.append(dict(zip(sdrlistsubkey, items)))
	
isVerbose = '_VERBOSE' in os.environ
isTry = '_Try' in os.environ

sqlfile = sdrlistresult + '.sql'

fhsql = open(sqlfile, 'w+')

fhsql.write('use server_management;\n')

smt = {
	'insert_time': insert_time,
	'server_id': server_id,
	'json': json.dumps({ipmicmd:sdrlistarray})
}

sqlsmt = "call insert_server_sdr_list_json('{insert_time}', '{server_id}', '{json}');\n".format(**smt)

fhsql.write(sqlsmt)

singlesqlfmt = "call insert_server_sdr_list('{insert_time}', '{server_id}', " + ', '.join(["'{" + subkey +"}'" for subkey in sdrlistsubkey]) + ");\n"
for sdrlist in sdrlistarray:
	obj = sdrlist
	obj['insert_time'] = insert_time
	obj['server_id'] = server_id
	
	singlesdr = singlesqlfmt.format(**obj)
	fhsql.write(singlesdr)

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

	
	
import sys,re,os,json,datetime,subprocess,shlex

# print(sys.argv[1])

selsaveresult = sys.argv[1]
(ipmicmd1, ipmicmd2, server_id, insert_time_filename, ext) = re.split(r'[\_\.]', os.path.basename(selsaveresult))
insert_time_mtime = os.path.getmtime(selsaveresult) if os.path.isfile(selsaveresult) else datetime.datetime.strptime(insert_time_filename, '%Y%m%d%H%M%S').timestamp()

ipmicmd = ipmicmd1 + ' ' + ipmicmd2
insert_time_basetime = datetime.datetime.strptime(insert_time_filename, '%Y%m%d%H%M%S')
insert_time_finishtime = datetime.datetime.fromtimestamp(insert_time_mtime)
insert_time = (insert_time_basetime + (insert_time_finishtime - insert_time_basetime) / 2).strftime('%Y%m%d%H%M%S')

selsavesubkey=['sensor_type', 'event_detail', 'sel_id', 'date', 'hour', 'sel_name', 'sel_condition', 'sel_tag']
lenselsavesubkey = len(selsavesubkey)

selsavearray=[]
if os.path.isfile(selsaveresult) and os.path.getsize(selsaveresult) > 0:
	fh = open(selsaveresult)
	lines = fh.readlines()
	fh.close()

	fhsave = open(selsaveresult + ".save.txt")
	linesave = fhsave.readlines()
	fhsave.close()

	if len(lines) != len(linesave):
		print('Error: inconsisit - ' + selsaveresult + ', ' + selsaveresult + ".save.txt")

	count = len(lines)

	for i in range(count):
		items = linesave[i].split(' ')[1:5:3]
		items.extend([item.strip() for item in lines[i].split('|')]) # assert_tag may empty, so we set sensor_type and event_detail at head
		lenitems = len(items)
		if lenselsavesubkey == lenitems:
			selsavearray.append(dict(zip(selsavesubkey, items)))
		elif lenselsavesubkey == lenitems + 1:
			selsavearray.append(dict(zip(selsavesubkey, items + [''])))
		else:
			print('ERROR: ' + lines[i])
			print('From - ' + selsaveresult)
			
	
isVerbose = '_VERBOSE' in os.environ
isTry = '_TRY' in os.environ

sqlfile = selsaveresult + '.sql'

fhsql = open(sqlfile, 'w+')

fhsql.write('use server_management;\n')

smt = {
	'insert_time': insert_time,
	'server_id': server_id,
	'json': json.dumps({ipmicmd:selsavearray})
}

sqlsmt = "call insert_server_sel_save_json('{insert_time}', '{server_id}', '{json}');\n".format(**smt)

fhsql.write(sqlsmt)

singlesqlfmt = "call Insert_server_sel_save_list('{insert_time}', '{server_id}', " + ', '.join(["'{" + subkey +"}'" for subkey in selsavesubkey]) + ");\n"
for selsave in selsavearray:
	obj = selsave
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

sqlcmd = '"{MYSQL}" -u{DBUSER} -p{DBPWD} < "{SQLFILE}"'.format(**obj)
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

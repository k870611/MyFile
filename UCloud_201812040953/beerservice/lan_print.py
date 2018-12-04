import sys,re,os,json,datetime,subprocess,shlex

# print(sys.argv[1])

lanprintresult = sys.argv[1]
(ipmicmd1, ipmicmd2, server_id, insert_time_filename, ext) = re.split(r'[\_\.]', os.path.basename(lanprintresult))
insert_time_mtime = os.path.getmtime(lanprintresult) if os.path.isfile(lanprintresult) else datetime.datetime.strptime(insert_time_filename, '%Y%m%d%H%M%S').timestamp()

ipmicmd = ipmicmd1 + ' ' + ipmicmd2
insert_time_basetime = datetime.datetime.strptime(insert_time_filename, '%Y%m%d%H%M%S')
insert_time_finishtime = datetime.datetime.fromtimestamp(insert_time_mtime)
insert_time = (insert_time_basetime + (insert_time_finishtime - insert_time_basetime) / 2).strftime('%Y%m%d%H%M%S')

lanprintdict={}
if os.path.isfile(lanprintresult):
	fh = open(lanprintresult)
	lines = fh.readlines()
	fh.close()

	curr = []
	for line in lines:
		items = [item.strip() for item in line.split(':')]
		colons = len(items)
		if len(curr) == colons:
			curr = [items[i] if items[i] != '' else curr[i] for i in range(colons)]
		else:
			curr = items

		if colons > 3:
			lanprintdict[curr[0]]=':'.join(curr[1:])
		elif colons == 3:
			if curr[0] not in lanprintdict:
				lanprintdict[curr[0]]={}
			if curr[1] not in lanprintdict[curr[0]]:
				lanprintdict[curr[0]][curr[1]]=curr[2]
			elif lanprintdict[curr[0]][curr[1]].__class__ is str:
				lanprintdict[curr[0]][curr[1]] = [lanprintdict[curr[0]][curr[1]], curr[2]]
			else:
				lanprintdict[curr[0]][curr[1]].append(curr[2])
		elif colons == 2:
			if curr[0] not in lanprintdict:
				lanprintdict[curr[0]]=curr[1]
			elif lanprintdict[curr[0]].__class__ is str:
				lanprintdict[curr[0]]=[lanprintdict[curr[0]],curr[1]]
			else:
				lanprintdict[curr[0]].append(curr[1])
			
isVerbose = '_VERBOSE' in os.environ
isTry = '_TRY' in os.environ

sqlfile = lanprintresult + '.sql'

fhsql = open(sqlfile, 'w+')

fhsql.write('use server_management;\n')

smt = {
	'insert_time': insert_time,
	'server_id': server_id,
	'json': json.dumps({ipmicmd:[lanprintdict]})
}

sqlsmt = "call insert_server_lan_print_json('{insert_time}', '{server_id}', '{json}');\n".format(**smt)

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

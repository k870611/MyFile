import sys,re,os,subprocess,shlex

arpresult = sys.argv[1]
ex = '_ex' if len(sys.argv) > 3 else ''

fh = open(arpresult)
lines = fh.readlines()
fh.close()

isVerbose = '_VERBOSE' in os.environ
isTry = '_TRY' in os.environ

sqlfile = arpresult + '.sql'

fhsql = open(sqlfile, 'w+')

fhsql.write('use server_management;\n')
	
for line in lines:
	thesearch = re.search(r'(?P<IPADRS>(?:\d+\.){3}\d+)\s+(?P<MACADRS>(?:\w+\-){5}\w+)',line)
	if thesearch is not None:
		sqlsmt = "call insert_server_arp('{MACADRS}','{IPADRS}');\n".format(**thesearch.groupdict())
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

import os, re, sys, time, shlex, subprocess

class AutoImportDb():
	def __init__(self):
		self.prefixes = ['Create_database', 'Create_', 'Insert_']
		self.priorities = [0,2,1,3]

	def get_priorities(self, sqlfile):
		for index in range(len(self.prefixes)):
			if sqlfile.startswith(self.prefixes[index]):
				return self.priorities[index]
		return len(self.priorities)
		
	def Run(self, scriptdir=None):
		sqlcommand = '"{mysql}" --user={dbuser} --password={dbpwd} < "{sqlfile}"'
		
		if scriptdir is None:
			scriptdir = os.path.join(os.path.realpath(os.path.dirname(sys.argv[0])), 'scripts')
		
		# read settings 
		fh = open("settings.cmd")
		lineitems = [re.split('[\s\=]', line.strip()) for line in fh.readlines()]
		fh.close()
		settings = {items[1].lower():' '.join(items[2:]) for items in lineitems if len(items)>2}

		# read sql script in order
		sqlfiles = [file for file in os.listdir(scriptdir) if file.endswith('.sql')]
		
		sortedsqlfiles = [os.path.join(scriptdir, sqlfile) for sqlfile in sorted(sqlfiles, key=self.get_priorities)]
		
		# execute sql scripts
		for sqlfile in sortedsqlfiles:
			settings['sqlfile'] = sqlfile
			cmd_string = sqlcommand.format(**settings)
			if '_Verbose' in os.environ:
				print('Execute: ' + cmd_string)
			
			try:
				cmdline = shlex.split(cmd_string, posix=False)
				cmdline[0] = cmdline[0].strip('"')
				cmdline[4] = cmdline[4].strip('"')
				lines = [line.strip().decode('utf-8') for line in subprocess.Popen(cmdline, shell=True, stderr=subprocess.PIPE).stderr.readlines()]
				errors = '\n'.join([line for line in lines if line.find('[Warning]')==-1])
				
				if errors != '':
					print(errors)
					
			except Exception as ex:
				print('Error: ' + str(ex))
				time.sleep(1)

if __name__ == '__main__':
	# script_folder = "scripts"
	auto_run = AutoImportDb()
	auto_run.Run()

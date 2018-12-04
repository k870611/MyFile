import os, sys, time, math, datetime, subprocess

print('Basic Enterprise Engineered Reporting Service (BEER Service)')

verbose = '_VERBOSE' in os.environ
nodelete = '_NODELETE' in os.environ

currdir = os.path.realpath(os.path.dirname(sys.argv[0]))
currdatetime = datetime.datetime.now()

cycletime = int(os.environ['CYCLETIME'])
basetime = int(os.environ['BASETIME'])

waittime = cycletime - (datetime.datetime.now().timestamp() % cycletime)

if verbose:
	print('Loop Manager Start')
	print('Current time: {} and wait 1st cycle {}'.format(currdatetime.strftime('%Y%m%d%H%M%S'), waittime))
time.sleep(waittime)

waittime = 0
subprocess.call(os.path.join(currdir, 'beer_service.cmd') + ' ' + 'Generate_Plan')

while waittime < basetime:
	ss = cycletime-math.floor(time.time() % cycletime)
	if verbose:
		print('Sleep ' + str(ss) + ' seconds')
	time.sleep(ss)
	subprocess.call(os.path.join(currdir, 'beer_service.cmd') + ' ' + 'Generate_Plan')
	waittime += cycletime

# time.sleep(waittime)

prevslotfile = ''
while True:
	currdatetime = datetime.datetime.now()
	currtime = currdatetime.strftime('%Y%m%d%H%M%S')
	currslottime = datetime.datetime.fromtimestamp(math.floor(currdatetime.timestamp() / cycletime) * cycletime)
	currslot = currslottime.strftime('%H%M%S')
	nextslottime = currslottime + datetime.timedelta(seconds=cycletime)
	
	currslotfile = os.path.join(os.environ['WORKDIR'], currslot)
	if prevslotfile!=currslotfile:
		if prevslotfile != '' and os.path.isfile(prevslotfile):
			pass # os.remove(prevslotfile)
		prevslotfile = currslotfile
	
	lines = []
	exist = False
	
	if os.path.isfile(currslotfile): # minute
		try:
			fh = open(currslotfile)
			lines = fh.readlines()
			fh.close()
			exist = True
		except:
			if verbose:
				print('Open current plan failed.  Sleep ... ' + str(cycletime))
	else:
		if verbose:
			print('no slot file ' + currslotfile)

	if not exist:
		sleeptime = cycletime - (datetime.datetime.now().timestamp() % cycletime)
		subprocess.call(os.path.join(currdir, 'beer_service.cmd') + ' ' + 'Generate_Plan')
		if 0 < sleeptime < cycletime:
			time.sleep(sleeptime)
		else:
			time.sleep(cycletime)
		continue

	for line in lines:
		line = line.strip()
	
		linesplit = line.split(' ')
		if len(linesplit) < 2:
			continue
		
		(thetime, thecmd) = linesplit
		if thetime > currtime:
			currtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
			sleeptime = (datetime.datetime.strptime(thetime,'%Y%m%d%H%M%S')-datetime.datetime.strptime(currtime,'%Y%m%d%H%M%S')).seconds
			if sleeptime < cycletime:
				if verbose:
					print('Wait for next task on.  Sleep ... ' + str(sleeptime))
				time.sleep(sleeptime)
			
			currtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
		
		try:
			if verbose:
				print(currtime + ' prcoessing ' + line)
			subprocess.call(os.path.join(currdir, 'beer_service.cmd') + ' ' + thecmd)
		except:
			pass
	
	currenttime = datetime.datetime.now()
	if currenttime < nextslottime:
		sleeptime = (nextslottime - currenttime).seconds
		if sleeptime < cycletime: 
			if verbose:
				print('Wait for next time slot.  Sleep ... ' + str(sleeptime))
			time.sleep(sleeptime)
		else:
			if verbose:
				print('Wait for next time slot.  Sleep ... ' + str(cycletime))
			time.sleep(cycletime)
		
		if not nodelete:
			try:
				os.remove(currslotfile)
			except:
				pass
	
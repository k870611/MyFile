import os, sys, math, datetime

if len(sys.argv) > 1:
	print(str(sys.argv))
	ss = int(sys.argv[1])
	bt = int(sys.argv[2])
	cy = int(sys.argv[3])
	print(datetime.datetime.fromtimestamp(math.floor((datetime.datetime.now().timestamp()+bt) / cy) * cy+ss).strftime('%Y%m%d%H%M%S'))
else:
	print(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
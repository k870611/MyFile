import os

from socket import gethostbyname, gethostname
# 获取本机IP地址
host = gethostbyname(gethostname())
print(host[:4])
# 获取ARP表
os.system('arp -a > temp.txt')

with open('temp.txt') as fp:
	for line in fp:
		line = line.split()[:2]
		print(line)
		if line and line[0].startswith(host[:4]) and (not line[0].endswith('255')):
			print(':'.join(line))

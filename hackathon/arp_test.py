import os
import sys
import platform

if len(sys.argv) > 1:
    if platform.system() == "Windows":
        os.system("arp -a {} > temp.txt".format(sys.argv[1]))
    else:
        os.system('arp -e {} > temp.txt'.format(sys.argv[1]))
else:
    if platform.system() == "Windows":
        os.system("arp -a > temp.txt")
    else:
        os.system('arp -e > temp.txt')

with open('temp.txt') as fp:
    for line in fp:
        if platform.system() == "Windows":
            info = line.split()[:2]

        else:
            info = line.split()[:3:2]
        
        print(info)

        if len(sys.argv) > 1 and info[0] == sys.argv[1]:
            print(' - '.join(info))

os.remove('temp.txt')

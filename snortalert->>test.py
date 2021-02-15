import os

os.system('grep -n 10000 /var/log/snort/alert > /tmp/test6.txt')
os.system('cat /var/log/snort/alert > /tmp/testfull.txt')

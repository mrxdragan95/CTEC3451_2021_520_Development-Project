import os

os.system("sudo grep -n 10000 /var/log/snort/alert > /tmp/test.txt")
os.system("sudo cat /var/log/snort/alert > /tmp/testfull.txt")

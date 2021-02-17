import os, glob

os.system('touch test.txt')
file_path = "/tmp/test/"
test = os.path.dirname(file_path)

try:
    os.stat(test)
except:
    os.mkdir(test)

#Loop Through the folder projects all files and deleting them one by one
for file in glob.glob("/tmp/test/*"):
    os.remove(file)
    print("Deleted " + str(file))
else:
  print("The file does not exist")

os.system('sudo chmod 777 /test/test.txt')
os.system('grep -n 10000 /var/log/snort/alert > /test/test.txt')
os.system('cat /var/log/snort/alert > /test/testfull.txt')
print("Done!")

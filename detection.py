# Detection implementation script - Dragan Butkovic -P2408503

# In Linux PIP is install from Python Package Index(PyPI). The PIP command 
# can be set up with the package manager for user’s distribution. 

# sudo apt install python3-pip



import subprocess 
import time
import os
import stat
import sys
import os.path
import shutil
import glob
from datetime import datetime
from subprocess import Popen, PIPE, STDOUT

#Cleaning the alerts and tcpdump.logs function -------------------------------------------------------------------------------------
def clean_alert():
    print("Clean alert")
    #Eliminating all the contents of alert <FILE> and staying file after recently added snort output (Using cp utilises with /dev/null)
    os.system('cp /dev/null /var/log/snort/alert')
    #Deleting only tcpdump.log.xxxxxxx
    os.system('rm -rf /var/log/snort/tcpdump.log*')

#Creating a directory with current time function -----------------------------------------------------------------------------------
def new_folder_log(curr_time): 
    #printing path for placing a new directory
    snort_folder_name = "New folder to /tmp/snortlog"
    print(snort_folder_name)
    #Finding the file's definite path related to the current working directory with current date
    file_path = "/tmp/snortlog" + curr_time + "/"
    #Returning the snort directory of snort folder 
    snortfile = os.path.dirname(file_path)

    try:
	# performing a stat system call on the given path
        os.stat(snortfile)
    except:
	# Creating a directory named path with numeric mode.
        os.mkdir(snortfile)

    print("New Snort folder is completed.")

# tshark function------------------------------------------------------------------------------------------------------------------- 
def run_tshark_on_local_machine(curr_time):
    func_name = "tshark_on_local_machine - "
    print(func_name + "start")
    #interface (eth0/wlan0/eth1) name on machine network
    interface_name = "eth0"
    #Creating a new packet capture (.pcap) before initiating  tshark
    capture_file_name = "/tmp/snortlog" + curr_time + "/" "Capture_" + interface_name + "_" + curr_time + ".pcap"
    #Waiting for 115 seconds while tshark running
    num_sec_to_sleep = 115
    print(func_name + "about to create capture with name:" + capture_file_name)
    #Executing the tshark with host on packet capture 
    p = subprocess.Popen(["tshark",
                          "-i", interface_name,
                          "-w", capture_file_name, 
			  "host", "192.168.253.136"],
                           stdout=subprocess.PIPE)
    #Stopping tshark in time.sleep
    time.sleep(num_sec_to_sleep)
    #Exiting the program successfully or Stopping running python and save packet capture
    #printing the end tshark 
    print(func_name + "end")

# Snort Function--------------------------------------------------------------------------------------------------------------------
def run_snort(curr_time):
    func_name = "Snort - "
    print(func_name + "start")
    #Reading the alert log directory
    snortlog = "/var/log/snort"
    #Reading the variety of Snort configuration options that can be set 
    snortconf = "/etc/snort/snort.conf"
    #Reading a new packet capture from tshark with current time
    capture_file_name = "/tmp/snortlog" + curr_time + "/" "Capture_" + interface_name + "_" + curr_time + ".pcap"
    #Waiting for 15 seconds while snort running
    num_sec_to_sleep = 15
    #Executing the snort with packet capture and putting into the snort.log and alert
    snort = subprocess.Popen(["snort", 
                          "-l", snortlog, "-c",
			  snortconf, "-r",
			  capture_file_name,
			  "-A", "fast"],
                          stdout=subprocess.PIPE)
    #Stopping snort in time.sleep
    time.sleep(num_sec_to_sleep)
    #Exiting the program successfully or Stopping running python and creating log
    snort.terminate()
    print(func_name + "end")

# snortlog to text Function---------------------------------------------------------------------------------------------------------
def snortlog_to_txt(curr_time):
    #Creating new snortlog.txt and open file in current directory with current date
    file_line = "/tmp/snortlog" + curr_time + "/snortlog_line.txt"
    file = open(file_line, "w")
    #Waiting for 3 seconds
    num_sec_to_sleep = 3
    file.close()
    #changing chmod() the mode of path to the passed numeric mode such as Read, write, and execute by owner, group, and others.  
    #sudo chmod 777 snortlog.txt 
    os.chmod(file_line, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)   
    #Copying the content of alert from snort output
    shutil.copy('/var/log/snort/alert', file_line)
    #Stopping in time.sleep
    time.sleep(num_sec_to_sleep)

# chmod 777 text Function-----------------------------------------------------------------------------------------------------------
def chmod_snort():
    #finding the absolute path of the .log* files in the snort directory
    for reading_logsnort in glob.glob('/var/log/snort/tcpdump.log.*'):
        #changing chmod() the mode of path to the passed numeric mode such as Read, write, and execute by owner, group, and others.  
        #sudo chmod 777 snortlog.txt 
	os.chmod(reading_logsnort, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
        print("Chmod tcpdump.log* is done")

# tcpdump.log to new packet capture Function---------------------------------------------------------------------------------------- 	
def snortlog_to_pcap(curr_time):
    #finding the absolute path of the .log* files in the snort directory 
    for reading_output in glob.glob('/var/log/snort/tcpdump.log.*'):
        #Creating a new packet capture from snort output
	capture_file_pcap = "/tmp/snortlog" + curr_time + "/" "Snortlog" + curr_time + ".pcap"
        #Waiting for 3 seconds
	num_sec_to_sleep = 3
        #Generating the tshark from tcpdump.log.xxxxxx to new packet capture
	tcpdump = subprocess.Popen(["tshark", "-r", reading_output,
                                    "-w", capture_file_pcap],
                                    stdout=subprocess.PIPE)
        #Stopping in time.sleep
	time.sleep(num_sec_to_sleep)
        #Exiting the program successfully
	tcpdump.terminate()
	
#Cleaning the alerts	
clean_alert()
#Getting the current data and time (year, month, day, hour, minute and second)
curr_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
#Executing the stopping running snort service in the background when only tshark runs 
os.system('systemctl stop snort')
#Creating a directory with current time
new_folder_log(curr_time)
#Executing the tshark for the host with current time
run_tshark_on_local_machine(curr_time)
#Exectung the snort from packet capture
run_snort(curr_time)
# Copying snortlog to text
snortlog_to_txt(curr_time)
# chmod 777 text
chmod_snort()
# Generating tcpdump.log to new packet capture
snortlog_to_pcap(curr_time)
#End
print("Successfully Done! :)")

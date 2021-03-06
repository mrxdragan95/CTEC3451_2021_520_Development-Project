


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
    #Removing all the contents of alert <FILE> and staying file after recently snort output (Using cp utilies with /dev/null)
    os.system('cp /dev/null /var/log/snort/alert')
    #Deleting only tcpdump.log.xxxxxxx
    os.system('rm -rf /var/log/snort/tcpdump.log*')

#Creating a directory with current time function -----------------------------------------------------------------------------------
def new_folder_log(curr_time): 
    #printing path where putting a new directory
    snort_folder_name = "New folder to /tmp/snortlog"
    print(snort_folder_name)
    #Finding the file's aboslute path relative to the current working directory with current date
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
    #Creating a new packet capture (.pcap) before starting tshark
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
    #Exiting the program successfully Or Stopping a running python and save packet capture
    p.terminate()
    #printing the end tshark 
    print(func_name + "end")

# Snort Function--------------------------------------------------------------------------------------------------------------------
def run_snort(curr_time):
    func_name = "Snort - "
    print(func_name + "start")
    #
    snortlog = "/var/log/snort"
    #
    snortconf = "/etc/snort/snort.conf"
    #
    capture_file_name = "/tmp/snortlog" + curr_time + "/" "Capture_" + interface_name + "_" + curr_time + ".pcap"
    #
    num_sec_to_sleep = 15
    #
    snort = subprocess.Popen(["snort", 
                          "-l", snortlog, "-c",
			  snortconf, "-r",
			  capture_file_name,
			  "-A", "fast"],
                          stdout=subprocess.PIPE)
    #
    time.sleep(num_sec_to_sleep)
    #
    snort.terminate()

def snortlog_to_txt(curr_time):
    #
    file_line = "/tmp/snortlog" + curr_time + "/snortlog_line.txt"
    #
    file = open(file_line, "w")
    #
    num_sec_to_sleep = 3
    file.close()
    #
    os.chmod(file_line, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)   
    #
    shutil.copy('/var/log/snort/alert', file_line)
    #
    time.sleep(num_sec_to_sleep)

#
def chmod_snort():
    #
    for reading_logsnort in glob.glob('/var/log/snort/tcpdump.log.*'):
        #
	os.chmod(reading_logsnort, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
        print("Chmod tcpdump.log* is done")

#	
def snortlog_to_pcap(curr_time):
    #
    for reading_output in glob.glob('/var/log/snort/tcpdump.log.*'):
        #
	capture_file_pcap = "/tmp/snortlog" + curr_time + "/" "Snortlog" + curr_time + ".pcap"
        #
	num_sec_to_sleep = 3
        #
	tcpdump = subprocess.Popen(["tshark", "-r", reading_output,
                                    "-w", capture_file_pcap],
                                    stdout=subprocess.PIPE)
        #
	time.sleep(num_sec_to_sleep)
        #
	tcpdump.terminate()
	
##Cleaning the alerts	
clean_alert()
#Getting the current data and time (year, month, day, hour, minute and second)
curr_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
#Executing the stopping running snort service in the background when only tshark runs 
os.system('systemctl stop snort')
#Creating a directory with current time
new_folder_log(curr_time)
#Executing the 
run_tshark_on_local_machine(curr_time)
#
run_snort(curr_time)
#
snortlog_to_txt(curr_time)
#
chmod_snort()
#
snortlog_to_pcap(curr_time)
#
print("Done")

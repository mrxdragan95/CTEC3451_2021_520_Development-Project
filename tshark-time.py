import subprocess
import schedule
import time
import os
from datetime import datetime

def run_tshark_on_local_machine(curr_time):
    func_name = "run_tshark_on_local_machine - "
    print(func_name + "start")
    interface_name = "eth0"
    capture_file_name = "/tmp/guyCapture_interface_" + interface_name + "_" + curr_time + ".pcap"
    num_sec_to_sleep = 30
    print(func_name + "about to create capture with name:" + capture_file_name)
    p = subprocess.Popen(["tshark",
                          "-i", interface_name,
                          "-w", capture_file_name, 
			  "host", "192.168.253.136"],
                           stdout=subprocess.PIPE)
    time.sleep(num_sec_to_sleep)
    p.terminate()
    print(func_name + "end")

def run_snort(curr_time):
    func_name = "run_snort - "
    print(func_name + "start")
    interface_name = "eth0"
    snortlog = "/var/log/snort"
    snortconf = "/etc/snort/snort.conf"
    capture_file_name = "/tmp/guyCapture_interface_" + interface_name+ "_" + curr_time + ".pcap"
    num_sec_to_sleep = 15
    s = subprocess.Popen(["snort", 
                          "-l", snortlog, "-c",
			  snortconf, "-r",
			  capture_file_name, 
			  "-A", "full"],
                          stdout=subprocess.PIPE)
    time.sleep(num_sec_to_sleep)
    s.terminate()

curr_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
os.system('systemctl stop snort')
run_tshark_on_local_machine(curr_time)
run_snort(curr_time)
print("Done")

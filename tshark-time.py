import subprocess
import time
from datetime import datetime

def run_tshark_on_local_machine():
    func_name = "run_tshark_on_local_machine - "
    print(func_name + "start")
    interface_name = "eth0"
    curr_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    capture_file_name = "/guyCapture_interface_" + interface_name + "_" + curr_time + ".pcap"
    num_sec_to_sleep = 120
    print(func_name + "about to create capture with name:" + capture_file_name)
    p = subprocess.Popen(["tshark",
                          "-i", interface_name,
                          "-w", capture_file_name, 
			                    "host", "192.168.253.137"],
                         stdout=subprocess.PIPE)
    time.sleep(num_sec_to_sleep)
    p.terminate()
    print(func_name + "end")

run_tshark_on_local_machine()

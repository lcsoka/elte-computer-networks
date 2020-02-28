import sys
import json
import subprocess
import datetime
import platform
from itertools import islice
from collections import deque
import threading
from multiprocessing.pool import ThreadPool

def first_n(file,n):
    return list(islice(file,n))

def last_n(file,n):
    return list(deque(file,n))

def get_host(line):
    return (line.rstrip('\n').split(','))[1]

def process_data(data):
    return {
        "target": data[0],
        "output": str(data[1])
    }

def ping(host):
    ping_iter_arg = '-c' # I use Mac OS so i use this as default...
    if platform.system() == 'Windows':
        ping_iter_arg = '-n'
    elif platform.system() == 'Linux':
        ping_iter_arg = '-c'

    p = subprocess.Popen(["ping", ping_iter_arg, "10", host], stdout=subprocess.PIPE)
    return process_data((host, p.communicate()[0].decode('utf-8')))

def traceroute(host):
    trace_cmd = 'traceroute' 
    if platform.system() == 'Windows':
        trace_cmd = 'tracert'
    elif platform.system() == 'Linux':
        trace_cmd = 'traceroute'

    trace_arg = '-m' 
    if platform.system() == 'Windows':
        trace_arg = '-h'
    elif platform.system() == 'Linux':
        trace_arg = '-m'

    p = subprocess.Popen([trace_cmd, trace_arg, "30", host], stdout=subprocess.PIPE)
    return process_data((host, p.communicate()[0].decode('utf-8')))

def create_json(data_name, data):
    return {
        "date": f"{datetime.datetime.now():%Y%m%d}",
        "system": platform.system(),
        data_name: data
    }

def run_ping_task(host_list, N):
    pool = ThreadPool(processes=N*2)
    result = pool.map(ping,host_list)
    with open("pings.json", "w") as out_file:
        json.dump(create_json("pings",result), out_file, indent=4)
    pool.close()
    pool.join()


def run_traceroute_task(host_list, N):
    pool = ThreadPool(processes=N*2)
    result = pool.map(traceroute,host_list)
    with open("traceroute.json", "w") as out_file:
        json.dump(create_json("traces",result), out_file, indent=4)
    pool.close()
    pool.join()


with open(sys.argv[1], "r") as f:
    print("File opened")
    N = 10
    host_list = map(get_host,(first_n(f,N) + last_n(f,N)))
    print("List parsed")
    run_ping_task(host_list,N)

    run_traceroute_task(host_list,N)
  
    print("DONE")
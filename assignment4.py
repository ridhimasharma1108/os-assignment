# ============================================================
# OS LAB ASSIGNMENT – 4
# System Calls, VM Detection, File Ops, Batch Processing
# ============================================================

import os
import subprocess
import multiprocessing
import logging
import time
import platform


# TASK 1 : Batch Processing Simulation


def batch_processing():
    print("\n--- TASK 1 : Batch Processing Simulation ---")

    scripts = ['script1.py', 'script2.py', 'script3.py']

    for script in scripts:
        print(f"Executing {script}...")
        try:
            subprocess.call(['python3', script])
        except Exception as e:
            print(f"Error executing {script}: {e}")


# TASK 2 : System Startup & Logging


logging.basicConfig(
    filename='system_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(processName)s - %(message)s'
)

def process_task(name):
    logging.info(f"{name} started")
    time.sleep(2)
    logging.info(f"{name} terminated")


def system_startup_logging():
    print("\n--- TASK 2 : System Startup & Logging ---")
    print("System Booting...")

    p1 = multiprocessing.Process(target=process_task, args=("Process-1",))
    p2 = multiprocessing.Process(target=process_task, args=("Process-2",))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("System Shutdown.")


# TASK 3 : System Calls + IPC (fork, exec, pipe)


def system_calls_ipc():
    print("\n--- TASK 3 : System Calls + IPC ---")

    r, w = os.pipe()
    pid = os.fork()

    if pid > 0:
        # Parent writes into pipe
        os.close(r)
        os.write(w, b"Hello from parent")
        os.close(w)
        os.wait()
    else:
        # Child reads
        os.close(w)
        msg = os.read(r, 1024)
        print("\nChild received:", msg.decode())
        os.close(r)
        os._exit(0)


# TASK 4 : VM Detection + Shell Commands


def detect_vm():
    print("\n--- TASK 4 : VM Detection ---")

    print("Kernel Version:", platform.release())
    print("User:", os.getlogin())

    print("\nChecking Virtualization Support:")
    try:
        result = subprocess.check_output("lscpu | grep 'Virtualization'", shell=True)
        print(result.decode())
    except:
        print("Virtualization info not available.")

    print("\nPossible VM Detected?" )
    vm_keywords = ["kvm", "vmware", "virtualbox", "qemu", "xen"]

    try:
        dmi = subprocess.check_output("dmesg | grep -i virtual", shell=True).decode().lower()
        if any(k in dmi for k in vm_keywords):
            print("YES - System seems to be running in a VM.")
        else:
            print("NO - Likely a physical machine.")
    except:
        print("Unable to detect using dmesg.")


# TASK 5 : CPU Scheduling Algorithms (FCFS, SJF, RR, Priority)


def fcfs(processes):
    print("\nFCFS Scheduling:")
    waiting = 0
    total_wt = 0
    total_tat = 0

    print("PID\tBT\tWT\tTAT")
    for pid, bt in processes:
        tat = waiting + bt
        print(f"{pid}\t{bt}\t{waiting}\t{tat}")
        total_wt += waiting
        total_tat += tat
        waiting += bt

    print("Average WT =", total_wt/len(processes))
    print("Average TAT =", total_tat/len(processes))


def sjf(processes):
    print("\nSJF Scheduling:")
    processes.sort(key=lambda x: x[1])  # Sort by burst

    fcfs(processes)


def priority_scheduling(processes):
    print("\nPriority Scheduling:")
    processes.sort(key=lambda x: x[2])  # Sort by priority

    wt = 0
    total_wt = 0
    total_tat = 0

    print("PID\tBT\tPR\tWT\tTAT")
    for pid, bt, pr in processes:
        tat = wt + bt
        print(f"{pid}\t{bt}\t{pr}\t{wt}\t{tat}")
        total_wt += wt
        total_tat += tat
        wt += bt

    print("Average WT =", total_wt/len(processes))
    print("Average TAT =", total_tat/len(processes))


def round_robin(processes, quantum):
    print("\nRound Robin Scheduling:")
    remaining = [bt for _, bt in processes]
    time_elapsed = 0
    n = len(processes)
    waiting = [0]*n
    turnaround = [0]*n

    done = False

    while not done:
        done = True
        for i in range(n):
            if remaining[i] > 0:
                done = False
                if remaining[i] > quantum:
                    time_elapsed += quantum
                    remaining[i] -= quantum
                else:
                    time_elapsed += remaining[i]
                    waiting[i] = time_elapsed - processes[i][1]
                    remaining[i] = 0

    for i in range(n):
        turnaround[i] = processes[i][1] + waiting[i]

    print("PID\tWT\tTAT")
    for i in range(n):
        print(f"{processes[i][0]}\t{waiting[i]}\t{turnaround[i]}")

    print("Average WT =", sum(waiting)/n)
    print("Average TAT =", sum(turnaround)/n)


def run_scheduling_all():
    print("\n--- TASK 5 : CPU Scheduling ---")

    processes_fcfs = [(1, 5), (2, 3), (3, 8)]
    processes_sjf = processes_fcfs.copy()
    processes_priority = [(1, 5, 2), (2, 3, 1), (3, 8, 3)]
    processes_rr = processes_fcfs.copy()

    fcfs(processes_fcfs)
    sjf(processes_sjf)
    priority_scheduling(processes_priority)
    round_robin(processes_rr, quantum=2)



if __name__ == "__main__":
    batch_processing()
    system_startup_logging()
    system_calls_ipc()
    detect_vm()
    run_scheduling_all()

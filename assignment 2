"""
OS Lab Assignment-2
System Startup, Process Creation, and Termination Simulation
Python 3.x | multiprocessing + logging
"""

import multiprocessing
import time
import logging


# Sub-Task 1: Logging Setup

logging.basicConfig(
    filename='process_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(processName)s - %(message)s'
)

# Sub-Task 2: Dummy Process Task

def system_process(task_name):
    logging.info(f"{task_name} started")
    time.sleep(2)   # simulate work
    logging.info(f"{task_name} ended")


# Main System Simulation

if __name__ == '__main__':
    print("System Starting...")

    # Sub-Task 3: Create Processes

    p1 = multiprocessing.Process(target=system_process, args=('Process-1',))
    p2 = multiprocessing.Process(target=system_process, args=('Process-2',))

    p1.start()
    p2.start()

    # Sub-Task 4: Termination

    p1.join()
    p2.join()

    print("System Shutdown.")

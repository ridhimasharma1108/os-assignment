#!/usr/bin/env python3
"""
process_management.py

OS Lab Assignment 1:
Process Creation and Management Using Python OS Module

Usage examples:
  # Task 1: create 3 children
  python3 process_management.py --task 1 --n 3

  # Task 2: execute commands in children (3 commands)
  python3 process_management.py --task 2 --cmd "ls -l" --cmd "date" --cmd "ps -ef"

  # Task 3: demonstrate zombie and orphan
  python3 process_management.py --task 3

  # Task 4: inspect process info from /proc for a given PID
  python3 process_management.py --task 4 --pid 1

  # Task 5: process prioritization with 4 CPU-bound children
  python3 process_management.py --task 5 --n 4

"""

import os
import sys
import time
import argparse
import subprocess
from typing import List, Tuple

def check_unix():
    if os.name != 'posix':
        print("Warning: This script is designed for Unix-like systems (Linux/macOS). Some features (fork, /proc) may not work on Windows.", file=sys.stderr)

# Task 1: Process Creation

def task1_create_children(n: int):
    """
    Create N children using os.fork().
    Each child prints its PID, PPID and a custom message.
    Parent waits for all children.
    """
    check_unix()
    if n <= 0:
        print("N must be >= 1")
        return

    children = []
    print(f"[Parent {os.getpid()}] Creating {n} child(ren)...")
    for i in range(n):
        pid = os.fork()
        if pid == 0:
            print(f"[Child {i+1}] PID={os.getpid()} PPID={os.getppid()} -> Hello from child {i+1}")
            time.sleep(0.5)
            os._exit(0)
        else:
            children.append(pid)

    for _ in children:
        try:
            finished_pid, status = os.wait()
            print(f"[Parent {os.getpid()}] Reaped child PID={finished_pid} with status {status}")
        except ChildProcessError:
            break

# Task 2: Command Execution Using exec

def parse_cmd_string(cmd: str) -> List[str]:
    # Simple split — assumes user provides commands like "ls -l" or "date"
    # For advanced parsing, shlex.split could be used.
    import shlex
    return shlex.split(cmd)

def task2_exec_in_children(commands: List[str]):
    """
    For each command in commands, fork a child and execute the command using os.execvp.
    """
    check_unix()
    if not commands:
        print("Provide at least one command")
        return

    children = []
    for i, cmd in enumerate(commands, start=1):
        args = parse_cmd_string(cmd)
        pid = os.fork()
        if pid == 0:
            try:
                print(f"[Child {os.getpid()}] Executing: {cmd}")
                os.execvp(args[0], args)
            except FileNotFoundError:
                print(f"[Child {os.getpid()}] Command not found: {args[0]}", file=sys.stderr)
            except Exception as e:
                print(f"[Child {os.getpid()}] Exec failed: {e}", file=sys.stderr)
            finally:
                os._exit(1)
        else:
            children.append(pid)

    for _ in children:
        try:
            finished_pid, status = os.wait()
            print(f"[Parent {os.getpid()}] Reaped child PID={finished_pid} (status={status})")
        except ChildProcessError:
            break

# Task 3: Zombie & Orphan process examples

def task3_zombie_and_orphan():
    """
    Demonstrate a zombie and an orphan:
    - Zombie: parent does not wait immediately (short sleep), child exits -> zombie visible via ps.
    - Orphan: parent exits while child sleeps -> child gets adopted by init (PID 1) or systemd.
    """
    check_unix()
    print("Demonstrating ZOMBIE:")
    pid = os.fork()
    if pid == 0:
        print(f"[Zombie-Child {os.getpid()}] I will exit now (become defunct until parent waits).")
        os._exit(0)
    else:
        print(f"[Parent {os.getpid()}] Sleeping for 2 seconds to allow zombie to appear in process table.")
        time.sleep(2)
        try:
            print("Running: ps -el | grep defunct")
            subprocess.run("ps -el | grep defunct || true", shell=True, check=False)
        except Exception as e:
            print("Unable to run ps to show defunct processes:", e)
        try:
            wpid, status = os.waitpid(pid, 0)
            print(f"[Parent {os.getpid()}] Reaped child {wpid} status={status}")
        except ChildProcessError:
            pass

    print("\nDemonstrating ORPHAN:")
    pid2 = os.fork()
    if pid2 == 0:
        print(f"[Orphan-Child {os.getpid()}] My initial PPID={os.getppid()}. I'll sleep 4 seconds.")
        time.sleep(4)
        print(f"[Orphan-Child {os.getpid()}] After sleep, my PPID={os.getppid()} (should be 1 or systemd if orphaned).")
        os._exit(0)
    else:
        print(f"[Parent {os.getpid()}] Exiting immediately to orphan the child {pid2}.")
        try:
            wpid, status = os.waitpid(pid2, 0)
            print(f"[Parent (after orphan simulation) {os.getpid()}] Reaped child {wpid} status={status}")
        except ChildProcessError:
            pass

# Task 4: Inspect process info from /proc

def safe_read_file(path: str) -> str:
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading {path}: {e}"

def task4_inspect_proc(pid: int):
    """
    Read and print:
      - Process name, state, memory usage from /proc/[pid]/status
      - Executable path from /proc/[pid]/exe (readlink)
      - Open file descriptors from /proc/[pid]/fd
    """
    check_unix()
    proc_base = f"/proc/{pid}"
    if not os.path.exists(proc_base):
        print(f"/proc/{pid} does not exist. Process may not be running or you don't have permission.")
        return

    status_path = os.path.join(proc_base, "status")
    print(f"---- /proc/{pid}/status ----")
    print(safe_read_file(status_path))

    exe_path = os.path.join(proc_base, "exe")
    try:
        exe_real = os.readlink(exe_path)
    except Exception as e:
        exe_real = f"Could not read exe link: {e}"
    print(f"\nExecutable (readlink): {exe_real}")

    fd_dir = os.path.join(proc_base, "fd")
    print(f"\nOpen file descriptors in /proc/{pid}/fd:")
    try:
        fds = os.listdir(fd_dir)
        if not fds:
            print("No file descriptors listed (or cannot access).")
        else:
            for fd in sorted(fds, key=lambda x: int(x)):
                path = os.path.join(fd_dir, fd)
                try:
                    target = os.readlink(path)
                    print(f"  fd {fd} -> {target}")
                except Exception as e:
                    print(f"  fd {fd} -> (could not read link: {e})")
    except Exception as e:
        print(f"Could not list {fd_dir}: {e}")

# Task 5: Process prioritization (nice)

def cpu_intensive_task(iterations: int):
    # Simple CPU-bound loop
    s = 0
    for i in range(iterations):
        s += i * i
    return s

def task5_prioritization(n_children: int):
    """
    Create n_children CPU-bound children, assign different nice() values,
    and observe execution order via completion timestamps.
    """
    check_unix()
    if n_children <= 0:
        print("Provide n_children >= 1")
        return

    children = []
    results = []
    iterations = 10_000_00  # adjust to produce measurable CPU time; reduce if too slow

    print(f"[Parent {os.getpid()}] Spawning {n_children} CPU-intensive children with different nice values.")
    for i in range(n_children):
        pid = os.fork()
        if pid == 0:
            nice_value = i * 5  # 0,5,10,...
            try:
                os.nice(nice_value)
            except Exception as e:
                print(f"[Child {os.getpid()}] Could not set nice to {nice_value}: {e}", file=sys.stderr)
            start = time.time()
            cpu_intensive_task(iterations)
            end = time.time()
            duration = end - start
            print(f"[Child {os.getpid()}] nice={nice_value} finished in {duration:.3f}s")
            os._exit(0)
        else:
            children.append(pid)

    print(f"[Parent {os.getpid()}] Waiting for children to finish...")
    while children:
        try:
            wpid, status = os.wait()
            if wpid in children:
                print(f"[Parent {os.getpid()}] Child {wpid} finished (status={status}).")
                children.remove(wpid)
        except ChildProcessError:
            break

    print("[Parent] All children reaped. Observe the printed durations above to see scheduler impact.")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process Management Tasks (OS Lab)")
    parser.add_argument('--task', '-t', type=int, choices=[1,2,3,4,5], required=True,
                        help="Task number to run (1-5)")
    parser.add_argument('--n', type=int, default=2, help="Number of child processes (for tasks 1 & 5)")
    parser.add_argument('--cmd', '--command', dest='cmds', action='append', help="Command to execute (task 2). Use multiple --cmd for multiple commands.")
    parser.add_argument('--pid', type=int, help="PID to inspect for task 4")
    return parser.parse_args()

def main():
    args = parse_args()
    t = args.task

    if t == 1:
        task1_create_children(args.n)
    elif t == 2:
        if not args.cmds:
            print("Provide at least one --cmd for task 2. Example: --cmd \"ls -l\"")
            sys.exit(1)
        task2_exec_in_children(args.cmds)
    elif t == 3:
        task3_zombie_and_orphan()
    elif t == 4:
        if not args.pid:
            print("Provide --pid for task 4. Example: --pid 1")
            sys.exit(1)
        task4_inspect_proc(args.pid)
    elif t == 5:
        task5_prioritization(args.n)
    else:
        print("Unknown task")

if __name__ == '__main__':
    main()

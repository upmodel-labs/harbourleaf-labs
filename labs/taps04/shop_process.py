"""Supplied. Starts and stops the practice shop (version 1) for the tests. Read it, do not edit it.

start_shop(port) starts the shop on that port and waits until /health answers.
It stops with an error when the shop process exits at once, for example because an old shop
still holds the port: an address that answers is not proof that it is your shop.
stop_shop(process) stops the shop.
If the environment variable SHOP_SLOW is set, the shop starts with --slow (answers take 1.5 to 3 seconds).
"""
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

SERVER = Path(__file__).parent / "webshop" / "server.py"


def start_shop(port):
    command = [sys.executable, str(SERVER), "--port", str(port)]
    if os.environ.get("SHOP_SLOW"):
        command.append("--slow")
    process = subprocess.Popen(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        if process.poll() is not None:
            raise RuntimeError(f"The shop did not start on port {port}. Is an old shop still running there?")
        try:
            with urllib.request.urlopen(f"http://localhost:{port}/health", timeout=1) as answer:
                if answer.status == 200:
                    time.sleep(0.3)
                    if process.poll() is not None:
                        raise RuntimeError(f"Port {port} answered, but not from the shop this run started.")
                    return process
        except OSError:
            time.sleep(0.2)
    stop_shop(process)
    raise RuntimeError(f"The shop did not answer on port {port} within 15 seconds.")


def stop_shop(process):
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()

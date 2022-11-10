import os

import psutil


def terminate_server():
    for i in psutil.process_iter():
        if i.name() == "python3":
            if i.cmdline()[1] == "server/server.py":
                i.terminate()


def server_run():
    os.popen("sh test_run.sh")

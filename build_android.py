import os
import time

t1 = time.time()

if os.name != "posix":
    exit()

cmds = [
    "pip3 install --user --upgrade buildozer",
    "sudo apt update",
    "sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev",
    "pip3 install --user --upgrade Cython==0.29.33 virtualenv  # the --user should be removed if you do this in a venv",
    "export PATH=$PATH:~/.local/bin/",
    "buildozer init",
    "buildozer android debug"
]

for cmd in cmds:
    os.system(cmd)

time_taken = int((time.time()-t1)*1000)

print("Time taken: " + str(time_taken) + "ms")

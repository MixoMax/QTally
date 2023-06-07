import os

#check if auto-py-to-exe is installed

r = os.system("python -m pip show auto-py-to-exe")

if r != 0:
    os.system("pip install auto-py-to-exe")


os.system("auto-py-to-exe")
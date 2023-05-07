import matplotlib.pyplot as plt
import csv
import os

os.chdir(f"C:/Users/{os.getlogin()}/Documents")

csv_path = "./count.csv"

with open(csv_path, "r") as f:
    reader = csv.reader(f)
    data = list(reader)

timestamps_relative = [data[i][0] for i in range(len(data))]
counts = [int(data[i][1]) for i in range(len(data))]
timestamps_abs = [data[i][2] for i in range(len(data))]  # convert to integer


fig, ax = plt.subplots()

ax.plot(timestamps_abs, counts)
ax.set_xlabel("Time")
ax.set_ylabel("Count")
ax.legend(["Count"])

ax.set_xticklabels(timestamps_relative)


plt.show()

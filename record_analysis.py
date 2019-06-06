import time
import matplotlib.pyplot as plt

timestamps = []
records = []
f = open("records.log", 'r')
number = int(f.readline()[8:-1])
# records.append(number)
for line in f.readlines():
    timestamps.append(time.mktime(time.strptime(line[6:26], "%Y-%m-%d  %H:%M:%S")))
    if line[28] == '+':
        number += int(line[29:-1])
    elif line[28] == '-':
        number -= int(line[29:-1])
    records.append(number)
f.close()

# plt.scatter(timestamps, records, marker='.')
for i in range(1, len(timestamps)):
    timestamp = timestamps[i]
    number = records[i]
    [marker, color] = ['^', 'b'] if number > records[i-1] else ['v', 'r']
    plt.scatter(timestamp, number, color=color, marker=marker, s=20)
plt.plot(timestamps, records, color='g', linewidth=1)
plt.title("Words not remembered (from 2019-05-21  21:00:31)")
plt.show()

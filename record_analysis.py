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

plt.scatter(timestamps, records, marker='.')
plt.plot(timestamps, records)
plt.title("Words not remembered (from 2019-05-21  21:00:31)")
plt.show()

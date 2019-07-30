import time
# from datetime import datetime
import re
import matplotlib.pyplot as plt
import getopt
import sys
import numpy as np

timestamps = []
num_hits_list = []
num_miss_list = []

file = "log.E2C"
opts, _ = getopt.getopt(sys.argv[1:], "", ["log="])
# print(opts)
for opt, arg in opts:
    if opt == "--log":
        file = arg

# print(file)
# start_date = "Date: 2019-05-15  20:59:39" if file == "log.E2C" else "Date: 2019-05-15  21:03:00"
f = open(file, 'r')
line = f.readline()
# while not line.startswith(start_date):
#    line = f.readline()

while line.startswith("Date"):
    # print(line[6:-1])
    date = time.strptime(line[6:-1], "%Y-%m-%d  %H:%M:%S")
    timestamps.append(time.mktime(date))
    _ = f.readline()  # Number
    # Get hit number
    hit_line = f.readline()
    start, end = re.search("\\d+", hit_line).span()
    num_hits_list.append(int(hit_line[start:end]))
    # Get miss number
    miss_line = f.readline()
    start, end = re.search("\\d+", miss_line).span()
    num_miss_list.append(int(miss_line[start:end]))
    _ = f.readline()  # Blank
    line = f.readline()
f.close()
# print(num_hits_list)
# num_hits_list = np.array(num_hits_list)
# num_miss_list = np.array(num_miss_list)
# num_total_list = num_hits_list + num_miss_list
num_total_list = [num_hits_list[i]+num_miss_list[i] for i in range(len(num_hits_list))]
# for i in range(len(num_hits_list)):
#     num_total_list.append(num_hits_list[i]+num_miss_list[i])
plt.plot(timestamps, num_total_list, color='r', linewidth=1)
plt.scatter(timestamps, num_total_list, color='r', marker='.')
plt.plot(timestamps, num_hits_list, color='b', linewidth=1)
plt.scatter(timestamps, num_hits_list, color='b', marker='.')
for i in range(len(timestamps)):
    timestamp = timestamps[i]
    plt.plot([timestamp, timestamp], [0, num_hits_list[i]], color='b', linestyle='--', linewidth=0.5)
    plt.plot([timestamp, timestamp], [num_hits_list[i], num_total_list[i]], color='r', linestyle=':', linewidth=0.5)
# avg_num_hits = 1.0 * sum(num_hits_list) / len(num_hits_list)
# print(avg_num_hits)
# plt.plot([timestamps[0],timestamps[-1]], [avg_num_hits] * 2, color='g')
number = 20
# avg_num_hits = [1.0*sum(num_hits_list[:i+1])/(i+1) for i in range(len(num_hits_list)) if i < number]
avg_num_hits = []
for i in range(len(num_hits_list)):
    if i < number:
        avg_num_hits.append(1.0 * sum(num_hits_list[:i + 1]) / (i + 1))
    else:
        avg_num_hits.append(1.0 * sum(num_hits_list[i - number + 1: i + 1]) / number)
plt.plot(timestamps, avg_num_hits, color='g')
title = "English to Chinese" if file == "log.E2C" else "Chinese to English"
# plt.title(title+' (from '+start_date[6:]+')')
plt.title(title)
plt.show()

rate_hits = np.array([1.0*num_hits_list[i]/num_total_list[i] for i in range(len(num_hits_list))])
# mean_rate_hits = np.mean(rate_hits)
# std_rate_hits = np.std(rate_hits)
plt.scatter(timestamps, rate_hits, color='b', marker='.')
plt.plot(timestamps, rate_hits, color='b', linewidth=1)
# mean_rate_hits = np.array([np.mean(rate_hits[:i+1]) for i in range(rate_hits.shape[0])])
# std_rate_hits = np.array([np.std(rate_hits[:i+1]) for i in range(rate_hits.shape[0])])
mean_rate_hits = []
std_rate_hits = []
for i in range(rate_hits.shape[0]):
    if i < number:
        mean_rate_hits.append(np.mean(rate_hits[:i + 1]))
        std_rate_hits.append(np.std(rate_hits[:i + 1]))
    else:
        mean_rate_hits.append(np.mean(rate_hits[i - number + 1:i + 1]))
        std_rate_hits.append(np.std(rate_hits[i - number + 1:i + 1]))
mean_rate_hits = np.array(mean_rate_hits)
std_rate_hits = np.array(std_rate_hits)
plt.plot(timestamps, mean_rate_hits, color='g')
plt.plot(timestamps, mean_rate_hits+std_rate_hits, color='r', linestyle='--')
plt.plot(timestamps, mean_rate_hits-std_rate_hits, color='r', linestyle='--')
# plt.plot([timestamps[0], timestamps[-1]], [mean_rate_hits]*2, color='g')
# plt.plot([timestamps[0], timestamps[-1]], [mean_rate_hits+std_rate_hits]*2, color='r', linestyle='--')
# plt.plot([timestamps[0], timestamps[-1]], [mean_rate_hits-std_rate_hits]*2, color='r', linestyle='--')
plt.ylim([0, 1])
# plt.title(title + " (hits / total, from " + start_date[6:] + ')')
plt.title(title + " (hits / total)")
plt.show()

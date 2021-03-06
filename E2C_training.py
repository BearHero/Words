import random
import os
import time

up_limit = 5
forgetting_time = 10 * 24 * 3600  # seconds

current_time = time.time()

f = open("words.inf", 'r')
head = f.readline()
word_list = [line.strip().split('\t') for line in f.readlines()]
f.close()

valid_word_list = []
for index in range(len(word_list)):
    if word_list[index][0] == "on":  # index 0: state == on
        valid_word_list.append(index)
    else:  # index 0: state == off
        last_time = word_list[index][-1]
        last_time = time.mktime(time.strptime(last_time, "%Y-%m-%d  %H:%M:%S"))
        if current_time - last_time >= forgetting_time:
            valid_word_list.append(index)
# valid_word_list = [index for index in range(len(word_list)) if word_list[index][0] == "on" or word_list[index][-1]]
random.shuffle(valid_word_list)  # shuffle the word list before selecting

print('*'*50)
number = int(input("Number: "))
if number > len(word_list):
    print("The number of selected words is too big!")
    os.system("pause")
selected_word_list = valid_word_list[:number]

words_hit = []
words_missed = []
off_words = 0
for index in selected_word_list:
    print('-'*50)
    print("Index: "+str(selected_word_list.index(index)+1))
    current_word = word_list[index][1]  # index 1: word
    print("Words: \033[0;31m%s\033[0m" % current_word)
    remember = input("Remember? ")
    print("Pronounce: " + word_list[index][2])  # index 2: pronounce
    print("Mean: \033[0;31m%s\033[0m" % word_list[index][3])  # index 3: mean
    print("Extend: " + word_list[index][-2])  # index -2: extend
    print("Last Time: " + word_list[index][-1])  # index -1: last_time
    hits = int(word_list[index][4])  # index 4: hits
    miss = int(word_list[index][5])  # index 5: miss
    if remember == current_word or remember == "yes":
        hit_flag = True
        print("\033[0;33m%s\033[0m" % "HIT!")
        word_list[index][4] = str(hits+1)  # index 4: hists
        words_hit.append(current_word)
        not_remember = input("Really remember? ")
        if not_remember and not_remember != "yes":
            hit_flag = False
            print("\033[0;34m%s\033[0m" % "MISSED!")
            words_missed.append(words_hit.pop())
            word_list[index][4] = str(hits)  # index 4: hists
            word_list[index][5] = str(miss+1)  # index 5: miss
    else:
        hit_flag = False
        print("\033[0;34m%s\033[0m" % "MISSED!")
        word_list[index][5] = str(miss+1)  # index 5: miss
        words_missed.append(current_word)
    hits = int(word_list[index][4])  # index 4: hits
    miss = int(word_list[index][5])  # index 5: miss
    print("(HITS: "+str(hits)+", MISS: "+str(miss)+')')
    if not hit_flag:
        continue
    if hits - miss >= up_limit:
        word_list[index][-1] = time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(current_time))  # index -1: last_time
        if word_list[index][0] == "on":
            word_list[index][0] = "off"  # index 0: state
            print("\033[0;33m%s\033[0m" % "(On -> Off)")
            off_words += 1
        else:  # state = off
            print("\033[0;33m%s\033[0m" % "(Off -> Off)")

if off_words:
    f_record = open("records.log", 'a')
    f_record.write("Date: "+time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(current_time))+', -'+str(off_words)+'\n')
    f_record.close()

f = open("words.inf", 'w')
f.write(head)
for word in word_list:
    line = '\t'.join(word) + '\n'
    f.write(line)
f.close()

training_log_path = "log.E2C"
if not os.path.isfile(training_log_path):
    os.system("touch "+training_log_path)
f = open(training_log_path, 'a')
f.write("Date: " + time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(current_time)) + '\n')
f.write("Number: " + str(number) + '\n')
f.write("HIT (" + str(len(words_hit)) + "): " + ', '.join(words_hit) + '\n')
f.write("MISSED (" + str(len(words_missed)) + "): " + ', '.join(words_missed) + '\n\n')

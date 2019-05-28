import time

count = 0
f_word = open("words.inf", 'a')
while True:
    print('+'*50)
    word = input("\033[0;31m%s\033[0m" % "Word: ")
    # word = input("Word: ")
    if not word:
        break
    pronounce = input("Pronounce: ")
    mean = input("Mean: ")
    extend = input("Extend: ")
    if not extend:
        extend = 'NULL'
    state = "on"
    hits = '0'
    miss = '0'
    line = state + '\t' + word + '\t/' + pronounce + '/\t' + mean + '\t' + hits + '\t' + miss + '\t' + extend + '\n'
    f_word.write(line)
    count += 1
f_word.close()
if count:
    f_record = open("records.log", 'a')
    f_record.write("Date: "+time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))+', +'+str(count)+'\n')
    f_record.close()

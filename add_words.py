f = open("words.inf", 'a')
while True:
    print('+'*10)
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
    f.write(line)
f.close()

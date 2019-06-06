date_to_words = {}


def get_date_to_words(file_name):
    f = open(file_name, 'r')
    line = f.readline()  # Date: ????-??-??  ??:??:??
    while line:
        the_date = line[6:-1]
        _ = f.readline()  # Number: ?
        line = f.readline()  # HIT (?): x, ..., x
        colon_index = line.index(':')
        words = line[colon_index + 2:-1]
        if words:
            words = words.split(", ")
            date_to_words[the_date] = words
        _ = f.readline()  # MISSED (?): x, ..., x
        _ = f.readline()  # Black line
        line = f.readline()  # Date: ????-??-??  ??:??:?? OR NULL
    f.close()


get_date_to_words("log.E2C")
get_date_to_words("log.C2E")
sorted_date_words = sorted(date_to_words.items(), key=lambda x: x[0], reverse=True)
# print(sorted_date_words)

words = []
f = open("old_words.inf", 'r')
_ = f.readline()  # state   word    pronounce       mean    hits    miss    extend
for line in f.readlines():
    line_list = line.strip().split('\t')
    if line_list[0] == "off":  # State
        word = line_list[1]  # Word
        for i in range(len(sorted_date_words)):
            if word in sorted_date_words[i][1]:
                last_date = sorted_date_words[i][0]
                break
        line_list.append(last_date)
    else:  # State = on
        line_list.append("NULL")
    words.append(line_list)
f.close()

f = open("words.inf", 'w')
f.write("state\tword\tpronounce\tmean\thits\tmiss\textend\tlast_dates\n")
for line_list in words:
    f.write('\t'.join(line_list)+'\n')
f.close()

import json
import time
import random
import os

words_path = "words.inf"
log_path = "records.log"
log_e2c = "log.E2C"
log_c2e = "log.C2E"

up_limit_A = 5
up_limit_G = 3
forget_time = 30 * 24 * 3600  # seconds


def add_words():
    # Read the words as a dictionary from words_path
    f = open(words_path, "r")
    words_dict = json.loads(f.readline())
    f.close()

    # Add some words
    count = 0
    while True:
        print("+" * 50)
        word = input("\033[0;31mWord: \033[0m")
        
        if word == "#delete":
            previous_word = input("\033[0;31mError word: \033[0m")
            if previous_word not in words_dict:
                print("\033[0;31mThe ERROR word [%s] is NOT in the LIB!\033[0m" % previous_word)
                continue
            del words_dict[previous_word]
            f = open(log_path, "a")
            f.write("Date: " + time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time())) + ', -1\n')
            f.close()
            continue
        
        if not word:
            break
        
        if word in words_dict:
            print("\033[0;31mThis word is in the dictionary!\033[0m")
            print("Word: " + word + " (" + words_dict[word]["type"] + ")")
            print("Pronounce: /" + words_dict[word]["pronounce"] + "/")
            print("Mean: " + words_dict[word]["mean"])
            if words_dict[word]["sentence"]:
                print("Sentence: " + words_dict[word]["sentence"])
            to_continue = input("To continue? (y/n)")
            if not to_continue or to_continue in ["y", "yes"]:
                continue
            else:
                break

        word_type = input("Type: ")  # G-General, A-Academic
        pronounce = input("Pronounce: ")
        mean = input("Mean: ")
        sentence = input("Sentence: ")
        hits = 0
        misses = 0
        words_dict[word] = {"type": word_type, "pronounce": pronounce, "mean": mean, "sentence": sentence,
                            "hits": hits, "misses": misses}
        count += 1

    # Update the log
    if count:
        f = open(log_path, "a")
        f.write("Date: " + time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
                + ', +' + str(count) + '\n')
        f.close()

    print("+" * 50)
    f = open(words_path, "w")
    f.write(json.dumps(words_dict))
    f.close()


def train(e2c=True):
    current_time = time.time()

    f = open(words_path, "r")
    words_dict = json.loads(f.readline())
    f.close()

    selected_words = []
    for word, info in words_dict.items():
        up_limit = up_limit_A if info["type"] == "A" else up_limit_G
        if info["hits"] - info["misses"] >= up_limit:
            assert "last time" in info
            last_time = info["last time"]
            last_time = time.mktime(time.strptime(last_time, "%Y-%m-%d  %H:%M:%S"))
            if current_time - last_time >= forget_time:
                selected_words.append(word)
        else:
            selected_words.append(word)

    print("*" * 50)
    number = int(input("Number = "))
    assert number <= len(selected_words)
    random.shuffle(selected_words)
    selected_words = selected_words[:number]
    words_hit = []
    words_miss = []
    remembered_words = 0
    for word in selected_words:
        info = words_dict[word]
        item = word + " (" + info["type"] + ")" if e2c else info["mean"]
        check = word + " (" + info["type"] + ")" if not e2c else info["mean"]
        print("-" * 50)
        print("\033[0;31mItem: %s\033[0m" % item)
        remember = input("Remember?")
        print("Check: " + check)
        print("Pronounce: /" + info["pronounce"] + "/")
        if info["sentence"]:
            print("Sentence:" + info["sentence"])
        if "last time" in info:
            print("Last Time: " + info["last time"])
        if remember in ["", "y", "yes", word, info["mean"]]:
            print("\033[0;33m%s\033[0m" % "HIT!")
            remember = "HIT"
            info["hits"] += 1
            words_hit.append(word)
        else:
            print("\033[0;34m%s\033[0m" % "MISS!")
            remember = "MISS"
            info["misses"] += 1
            words_miss.append(word)
        confirm = input("Really %s?" % remember)
        if confirm not in ["", "y", "yes"]:
            if remember == "HIT":  # Missed in fact
                remember = "MISS"
                info["hits"] -= 1
                info["misses"] += 1
                words_miss.append(words_hit.pop())
            else:  # Hit in fact
                remember = "HIT"
                info["hits"] += 1
                info["misses"] -= 1
                words_hit.append(words_miss.pop())
        print("(HITS: " + str(info["hits"]) + ", MISS: " + str(info["misses"]) + ")")
        up_limit = up_limit_A if info["type"] == "A" else up_limit_G
        if info["hits"] - info["misses"] >= up_limit:
            assert not ("last time" not in info and remember == "MISS")
            if "last time" not in info:
                remembered_words += 1
            if remember == "HIT":
                info["last time"] = str(current_time)
                print("\033[0;33mCurrent Time%s\033[0m" % info["last time"])
    assert set(words_hit).union(set(words_miss)) == set(selected_words)

    if remembered_words:
        f = open(log_path, 'a')
        f.write("Date: " + time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(current_time))
                + ', -' + str(remembered_words) + '\n')
        f.close()

    training_log_path = log_e2c if e2c else log_c2e
    if not os.path.isfile(training_log_path):
        os.system("touch " + training_log_path)
    f = open(training_log_path, 'a')
    f.write("Date: " + time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(current_time)) + '\n')
    f.write("Number: " + str(number) + '\n')
    f.write("HIT (" + str(len(words_hit)) + "): " + ', '.join(words_hit) + '\n')
    f.write("MISSED (" + str(len(words_miss)) + "): " + ', '.join(words_miss) + '\n\n')
    f.close()

    f = open(words_path, "w")
    f.write(json.dumps(words_dict))
    f.close()


def show_words():
    f = open(words_path, "r")
    words_dict = json.loads(f.readline())
    print("*" * 50)
    for word in words_dict.keys():
        print("\033[0;31mWords: %s\033[0m" % word)
        print("Pronounce: /" + words_dict[word]["pronounce"] + "/")
        print("Mean: " + words_dict[word]["mean"])
        print("Sentence: " + words_dict[word]["sentence"])
        print("*" * 50)
    f.close()


if __name__ == "__main__":
    add_words()
    show_words()

    train(e2c=True)
    train(e2c=False)

import json
import time

words_path = "words.inf"
log_path = "records.log"


def add_words():
    # Read the words as a dictionary from words.inf
    f = open(words_path, "r")
    words_dict = json.loads(f.readline())
    f.close()

    # Add some words
    count = 0
    while True:
        print("+" * 50)
        word = input("\033[0;31m%s\033[0m" % "Word: ")
        if not word:
            break
        if word in words_dict:
            print("\033[0;31m This word is in the dictionary!\033[0m")
            print("Pronounce: " + words_dict[word]["pronounce"])
            print("Mean: " + words_dict[word]["mean"])
            print("Sentence: " + words_dict[word]["sentence"])
            break
        pronounce = input("Pronounce: ")
        mean = input("Mean: ")
        sentence = input("Sentence: ")
        hits = 0
        misses = 0
        words_dict[word] = {"pronounce": pronounce, "mean": mean, "sentence": sentence,
                            "hits": hits, "misses": misses}
        count += 1
    print("+" * 50)
    f = open(words_path, "w")
    f.write(json.dumps(words_dict))
    f.close()

    # Update the log
    if count:
        f = open(log_path, "a")
        f.write("Date: " + time.strftime('%Y-%m-%d  %H:%M:%S', time.localtime(time.time()))
                       + ', +' + str(count) + '\n')
        f.close()


def show_words():
    f = open(words_path, "r")
    words_dict = json.loads(f.readline())
    print("*" * 50)
    for word, information in words_dict.items():
        print("\033[0;31mWords: %s\033[0m" % word)
        print("*" * 50)
    f.close()


if __name__ == "__main__":
    add_words()
    show_words()

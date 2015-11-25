import sys
import nltk


def window(coll, size):
    coll_len = len(coll)
    for i in range(coll_len):
        if i + size > coll_len:
            break
        else:
            yield tuple(coll[i:i + size])


for line in sys.stdin:
    timestamp, nick, msg = line.split(' ', 2)

    n = int(sys.argv[1])

    for ngram in set(window(nltk.word_tokenize(msg), n)):
        print(timestamp, nick, '__'.join(ngram))
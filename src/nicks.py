import sys

for line in sys.stdin:

    timestamp, nick, msg = line.split(' ', 2)

    print(nick)
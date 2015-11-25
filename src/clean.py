import sys
import errno
import re
import datetime
import time


def datetime_to_epoch(dt):
    return int(time.mktime(dt.timetuple()))


# Example log line: [2015/01/31][00:00:00] <nick> msg
# this regex captures this: "2015/01/31", "00:00:00", "nick" and "msg"
pattern = re.compile('\[(\d{4}/\d{2}/\d{2})\]\[(\d{2}:\d{2}:\d{2})\]\s<(.*)>\s(.*)')

sys.stderr.write('Starting conversion...\n')

for line in sys.stdin:
    match = pattern.match(line)
    if match is None:
        continue

    groups = match.groups()

    if not groups:
        sys.stderr.write('  > no groups captured for "' + line + '"\n')
        # if there was nothing captured, just continue
        continue

    date = groups[0]
    hour = groups[1]
    nick = groups[2]
    msg = groups[3]

    timestamp = datetime_to_epoch(
        datetime.datetime.strptime(date + ' ' + hour.strip('[]'), '%Y/%m/%d %H:%M:%S'))

    line = '{0} {1} {2}'.format(timestamp, nick, msg)

    try:
        print(line)
    except IOError as e:
        if e.errno == errno.EPIPE:
            # the next command in the chain as stopped reading.
            # just exit here
            sys.exit(0)
        else:
            raise e
import sys
from aggregate import aggregate


bucket_size = 1
line_filter = None

if len(sys.argv) > 1:
    bucket_size = int(sys.argv[1])

if len(sys.argv) > 2:
    line_filter = sys.argv[2]


res = aggregate(sys.stdin, bucket_size, line_filter)

for datetime, count in res:
    print(datetime.strftime("%s"), count, sep="\t")

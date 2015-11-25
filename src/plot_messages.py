import sys
import matplotlib.pyplot as plt
from aggregate import aggregate


bucket_size = 1

if len(sys.argv) > 1:
    bucket_size = int(sys.argv[1])


res = aggregate(sys.stdin, bucket_size)


plt.plot(*zip(*res))
plt.show()

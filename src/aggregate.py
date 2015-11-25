from datetime import timedelta, datetime


def aggregate(resource, bucket_size=10, line_filter=None):
    """
    Counts lines per bucket_size.

    Lines have be in the format "TIMESTAMP OTHER_STUFF"

    Bucket Size defaults to 10 minutes.

    :param resource: the resource to read lines from
    :param bucket_size: aggregation width in minutes
    :param line_filter: if the value is not None, only lines containing the string will be counted
    :return: list of aggregated messages [(START_DATE, COUNT), ...]
    """
    current = -1
    count = 0

    res = []

    for line in resource:
        t = datetime.fromtimestamp(int(line.split(' ')[0]))

        if current is -1:
            current = t

        if (t - current) <= timedelta(minutes=bucket_size):
            if line_filter is None or line_filter in line.lower():
                count += 1
        else:
            res.append((current, count))
            current = t
            count = 1

    res.append((current, count))  # add last tuple

    return res


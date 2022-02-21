from fei.ppds import *
from collections import Counter


class Shared():
    def __init__(self, size):
        self.counter = 0
        self.end = size
        self.elms = [0] * size


def increment(shared, mutex):
    mutex.lock()
    while shared.counter < shared.end:
        shared.elms[shared.counter] += 1
        shared.counter += 1
    mutex.unlock()

shared = Shared(1_000_000)
mutex = Mutex()

t1 = Thread(increment, shared, mutex)
t2 = Thread(increment, shared, mutex)

t1.join()
t2.join()

counter = Counter(shared.elms)
print(counter.most_common())

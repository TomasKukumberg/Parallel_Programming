from fei.ppds import *
from collections import Counter


class Shared():
    def __init__(self, size):
        """init class with counter (index to array),
        end (number of entries) and elms (array)"""
        self.counter = 0
        self.end = size
        self.elms = [0] * size


def increment(shared, mutex):
    """Increment value at index of array where shared.counter is currently "pointing".
    Mutex is used to avoid problems with multithreading. 
    First argument is the shared object and the rest of arguments are objects you want to use in this function."""
    while True:
        mutex.lock()
        if shared.counter >= shared.end:
            mutex.unlock()
            break
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

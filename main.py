"""
Copyright 2022 Tomas Kukumberg <tomas.kukumberg@centrum.sk>
This code is licensed under MIT license
This module is dealing with the 'dining savages' problem.
We have N number of savages, M number of portions and L number of cooks.
The goal is to sync savages and cooks
to continue eating and cooking when possible.
"""

from random import randint
from time import sleep
from fei.ppds import Thread, print, Semaphore, Mutex, Event

N = 3  # amount of savages
M = 6  # amount of food portions
L = 4  # amount of cooks


class SimpleBarrier():
    """
    This class implements a barrier using a counter,
    mutex to protect the counter from multiple accesses at the 'same' time
    and a barrier, which is just a semaphore initialized with 0.
    The barrier lets threads pass only when cnt is equal to N.
    Class members:
    N -> number of threads when we want to unlock the barrier.
    cnt -> currently waiting threads at the barrier
    mutex -> lock to protect the counter
    barrier -> semaphore initialized to 0
    """
    def __init__(self, N):
        """
        Init the SimpleBarrier class.
        Args: N -> number of threads when we want to unlock the barrier.
        """
        self.N = N
        self.cnt = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self):
        """
        Wait at the barrier if cnt is less than N,
        else let threads through the barrier.
        """
        self.mutex.lock()
        self.cnt += 1
        if self.cnt == self.N:
            self.cnt = 0
            self.barrier.signal(self.N)
        self.mutex.unlock()
        self.barrier.wait()


class Shared():
    """
    Class holding the servings which will be served to savages.
    Other sync mechanisms used to achieve correct cooking and eating.
    Class members:
    self.mutex -> protect the servings
    self.mutex2 -> protect the 'signalized_already' member
    self.full_pot -> semaphore that will signalize that pot is full to savages
    self.empty_pot -> event that will signalize to cooks
    that they should start cooking
    self.b -> barrier that will wait for all cooks to finish cooking
    self.signalized_already -> a helper boolean variable that checks
    if we've already signalized to savages that the pot is full.
    If it is true, it means one cook already signalized it
    to savages and other cooks won't have to signalize.
    """
    def __init__(self, m):
        """
        Initialize the Shared class.
        Args:
        m -> number of servings
        """
        self.mutex = Mutex()
        self.mutex2 = Mutex()
        self.servings = m
        self.full_pot = Semaphore(0)
        self.empty_pot = Event()
        self.b = SimpleBarrier(L)
        self.signalized_already = False


def eat(i):
    """
    Eating function called from the savages.
    Args:
    i -> savage id
    """
    print(f'savage {i} starts to eat')
    sleep(randint(50, 200) / 100)
    print(f'savage {i} finished eating')


def savage(i, shared):
    """
    Perform savage eating and signalize to cooks if pot is empty.
    Args:
    i -> savage id
    shared -> shared object described with help(Shared)
    """
    sleep(randint(1, 100) / 100)
    while True:
        shared.mutex.lock()
        if shared.servings == 0:
            print(f'savage {i}: empty pot')
            shared.empty_pot.signal()
            shared.full_pot.wait()
        print(f'savage {i}: take from pot')
        shared.servings -= 1
        shared.mutex.unlock()
        eat(i)


def cook(shared):
    """
    Perform cooking. If pot isn't empty, don't cook.
    Uses barrier to synchronize cooks.
    Args:
    shared -> shared object described with help(Shared)
    """
    while True:
        shared.empty_pot.wait()
        shared.signalized_already = False
        print('The cook is cooking')
        sleep(randint(50, 200) / 100)

        shared.b.wait()
        shared.mutex2.lock()
        if not shared.signalized_already:
            print(f'cook: {M} servings --> pot')
            shared.servings += M
            shared.full_pot.signal()
            shared.signalized_already = True
            shared.empty_pot.clear()
        shared.mutex2.unlock()


def main():
    """
    Main function which creates savages and cooks.
    """
    shared = Shared(0)
    savages = []
    for i in range(N):
        savages.append(Thread(savage, i, shared))

    for i in range(L):
        savages.append(Thread(cook, shared))

    for t in savages:
        t.join()

if __name__ == "__main__":
    main()

from random import randint
from time import sleep
from fei.ppds import Thread, Semaphore, Mutex, Event
from fei.ppds import print


class SimpleBarrier:
    """Class implementing a simple barrier using Events."""
    def __init__(self, N):
        """
        Parameters:
        N - number of threads
        C - counter
        M - mutex for sync
        T - event
        """
        self.N = N
        self.C = 0
        self.M = Mutex()
        self.T = Event()

    def wait(self):
        """
        Wait function, uses a mutex to increment a counter
        and if all threads happened,
        signal other threads with an Event to continue.
        Parameters: None
        Returns: None
        """
        self.M.lock()
        self.C += 1
        if self.C == self.N:
            self.C = 0
            self.T.signal()
        self.M.unlock()
        self.T.wait()
        self.T.clear()


def before_barrier(thread_id):
    """
    Prints thread id before the barrier.
    Arguments:
    thread_id - id of the current thread
    Returns: None
    """
    sleep(randint(1, 10) / 10)
    print(f'before barrier {thread_id}')


def after_barrier(thread_id):
    """
    Prints thread id after the barrier.
    Arguments:
    thread_id - id of the current thread
    Returns: None
    """
    print(f'after barrier {thread_id}')
    sleep(randint(1, 10) / 10)


def barrier_cycle(b1, b2, thread_id):
    """
    Calls before_barrier, wait and after_barrier methods
    to show the functionality of simple ADT barrier in a loop.
    Parameters:
    b1 - first barrier
    b2 - second barrier
    thread_id - id of the current thread
    Returns: None
    """
    while True:
        before_barrier(thread_id)
        b1.wait()
        after_barrier(thread_id)
        b2.wait()


THREADS = 10
sb1 = SimpleBarrier(10)
sb2 = SimpleBarrier(10)


threads = [Thread(barrier_cycle, sb1, sb2, i) for i in range(THREADS)]
[t.join() for t in threads]

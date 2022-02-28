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


def barrier_example(barrier, thread_id):
    """
    A simple function to demonstrate the functionality of an ADT barrier.
    Parameters:
    thread_id - id of the current thread
    Returns: None
    """
    sleep(randint(1, 10) / 10)
    print("vlakno %d pred barierou" % thread_id)
    barrier.wait()
    print("vlakno %d po bariere" % thread_id)


THREADS = 10
sb = SimpleBarrier(THREADS)

threads = [Thread(barrier_example, sb, i) for i in range(THREADS)]
[t.join() for t in threads]

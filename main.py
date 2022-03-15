"""
Copyright 2022 Tomas Kukumberg <tomas.kukumberg@centrum.sk>
This code is licensed under MIT license

This module is dealing with a 'nuclear factory' problem.
We have 3 sensors, 8 monitors and we are trying to synchronize
reading and writing in the best way possible.
"""

from fei.ppds import Mutex, Semaphore, Thread, Event, print
from time import sleep
from random import randint


class Lightswitch:
    """
    Implementation of the lightswitch sync pattern
    with the use of a mutex lock and counter.
    """
    def __init__(self):
        "Initialize the object with a mutex lock and counter variable."
        self.mutex = Mutex()
        self.counter = 0

    def lock(self, sem):
        """Lock the mutex lock in the lightswitch class."""
        self.mutex.lock()
        counter = self.counter
        self.counter += 1
        if self.counter == 1:
            sem.wait()
        self.mutex.unlock()
        return counter

    def unlock(self, sem):
        """Unlock the mutex lock in the lightswitch class."""
        self.mutex.lock()
        self.counter -= 1
        if self.counter == 0:
            sem.signal()
        self.mutex.unlock()


class ValidData:
    """
    Class used to signal an event to monitors
    when all 3 sensors measured a value."""
    def __init__(self):
        """
        Set Event for signalization,
        counter to count how many values were measured
        and mutex to protect the counter.
        """
        self.e = Event()
        self.c = 0
        self.m = Mutex()

    def try_signal(self):
        """
        Signal if count size is 3 or bigger.
        """
        self.m.lock()
        self.c = self.c + 1
        cnt = self.c
        self.m.unlock()
        if cnt >= 2:
            self.e.signal()


def init():
    """
    Spawns threads, uses semaphores and lightswitch.
    Calls methods which will start measuring data
    from sensors and then display this data
    on monitors using various synchronization patterns.
    """
    access_data = Semaphore(1)
    turniket = Semaphore(1)
    ls_monitor = Lightswitch()
    ls_cidlo = Lightswitch()
    valid_data = ValidData()

    for monitor_id in range(8):
        Thread(monitor, monitor_id, valid_data, turniket, ls_monitor,
               access_data)

    for cidlo_id in range(3):
        Thread(cidlo, cidlo_id, turniket, ls_cidlo, valid_data, access_data)


def monitor(monitor_id, valid_data, turniket, ls_monitor, access_data):
    """
    Monitor won't work until all 3 sensors had send the data.
    """
    valid_data.e.wait()

    while True:
        sleep(randint(40, 50)/1000)
        turniket.wait()
        pocet_citajucich_monitorov = ls_monitor.lock(access_data)
        turniket.signal()

        print(f'monit "{monitor_id:02d}": '
              f'pocet_citajucich_monitorov={pocet_citajucich_monitorov:02d}')
        ls_monitor.unlock(access_data)


def cidlo(cidlo_id, turniket, ls_cidlo, valid_data, access_data):
    """
    Sensors are passing through the turnstile until monitor locks it
    """
    while True:
        sleep(randint(50, 60) / 1000)
        turniket.wait()
        pocet_zapisujucich_cidiel = ls_cidlo.lock(access_data)
        turniket.signal()

        if cidlo_id == 1 or cidlo_id == 2:
            trvanie_zapisu = randint(10, 20) / 1000
        else:
            trvanie_zapisu = randint(20, 25) / 1000
        print(f'cidlo "{cidlo_id:02d}":  '
              f'pocet_zapisujucich_cidiel={pocet_zapisujucich_cidiel:02d}, '
              f'trvanie_zapisu={trvanie_zapisu:5.3f}')
        sleep(trvanie_zapisu)
        valid_data.try_signal()
        ls_cidlo.unlock(access_data)

if __name__ == '__main__':
    init()

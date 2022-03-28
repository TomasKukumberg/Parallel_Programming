"""
Copyright 2022 Tomas Kukumberg <tomas.kukumberg@centrum.sk>
This code is licensed under MIT license
This module is dealing with the 'barber and customers' problem.
"""

from random import randint
from time import sleep
from fei.ppds import Thread, print, Semaphore, Mutex, Event
from queue import Queue


N_CUSTOMERS = 8


class Shared():
    """Shared class which manages access to the queue.
    Uses mutex and semaphores to sync."""
    def __init__(self, N):
        """Init the class with number of space in the shop."""
        self.mutex = Mutex()
        self.mutex2 = Mutex()
        self.customer = Semaphore(0)
        self.barber = Semaphore(0)
        self.customerDone = Semaphore(0)
        self.barberDone = Semaphore(0)
        self.queue = Queue(N)

    def enterShop(self, i):
        """Customer enters a shop and either gets in queue
        or leaves if space is full.
        Takes id of customer as argument, returns None."""
        self.mutex2.lock()
        if self.queue.full():
            print(f'No space left in the shop. Customer {i} is leaving...')
        else:
            print(f'Customer {i} is waiting in the queue...')
            self.queue.put(i)
        self.mutex2.unlock()

    def leaveShop(self, i):
        """Customer leaves the shop. Takes id as argument, returns None."""
        print(f'Customer {i} is leaving the shop...')
        self.mutex.lock()
        self.queue.get()
        self.mutex.unlock()


def getHairCut(i):
    """Function for customer to get a haircut which
    simulates randomness with rand sleep.
    Takes id of customer as argument, returns None."""
    sleep(randint(1, 100) / 100)
    print(f"Customer {i} is getting a new haircut...")


def customer(i, shared):
    """Customer function which takes id of customer
    and shared object as arguments. Returns None."""
    while True:
        sleep(randint(1, 100) / 100)
        shared.enterShop(i)
        if i in shared.queue.queue:
            shared.mutex.lock()
            shared.customer.signal()
            shared.barber.wait()
            getHairCut(i)
            shared.customerDone.signal()
            shared.barberDone.wait()
            print(f"Customer {i} just got a new haircut!")
            shared.mutex.unlock()
            shared.leaveShop(i)


def cutHair():
    """Function for barber to cut customer's hair
    which simulates randomness with rand sleep.
    Returns None."""
    sleep(randint(1, 100) / 100)
    print(f"Barber is cutting customer's hair...")


def barber(shared):
    """Barber function which takes shared object as argument. Returns None."""
    while True:
        shared.customer.wait()
        shared.barber.signal()
        cutHair()
        shared.customerDone.wait()
        shared.barberDone.signal()


def main():
    """Main function of this module. Returns None."""
    shared = Shared(3)
    barberDude = Thread(barber, shared)
    customers = []

    for i in range(N_CUSTOMERS):
        customers.append(Thread(customer, i, shared))


if __name__ == "__main__":
    main()

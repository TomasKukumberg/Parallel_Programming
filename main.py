"""
Copyright 2022 Tomas Kukumberg <tomas.kukumberg@centrum.sk>
This code is licensed under MIT license
This module is dealing with the 'generators and scheduler' problem.
"""

from random import randint
import sched
from time import sleep

step = 2


def even(n):
    """Even generator function which yields even numbers.
    Takes n as argument which is a limit,
    yields even numbers until number < n + 1."""
    for i in range(0, n+1, step):
        sleep(randint(0, 2))
        yield i


def odd(n):
    """Odd generator function which yields odd numbers.
    Takes n as argument which is a limit,
    yields odd numbers until number < n + 1."""
    for i in range(1, n+1, step):
        sleep(randint(0, 2))
        yield i


def scheduler(queues):
    """Scheduler function which decides which task will go next.
    Takes queues as argument, which are all the tasks
    we want to manage by the scheduler. Returns None."""
    while True:
        try:
            for q in queues:
                print(next(q))
        except StopIteration:
            break

k1 = even(10)
k2 = odd(10)
queues = [k1, k2]

scheduler(queues)


from random import randint
import sched
from time import sleep

step = 2

def even(n):
    for i in range(0, n+1, step):
        sleep(randint(0,2))
        yield i

def odd(n):
    for i in range(1, n+1, step):
        sleep(randint(0,2))
        yield i

def scheduler(queues):
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
from fei.ppds import Mutex, Semaphore, Thread, print
from random import randint
from time import sleep
import matplotlib.pyplot as plt


class Shared():
    """Class which takes care of synchronization by using semaphores."""
    def __init__(self, N):
        self.finished = False
        self.mutex = Mutex()
        self.free = Semaphore(N)
        self.items = Semaphore(0)
        self.counter = 0


def producer(shared, ratio):
    """Function for the producer to manufacture a new object."""
    while True:
        shared.free.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        shared.counter += 1
        sleep(randint(1, 10)/ratio)
        shared.mutex.unlock()
        shared.items.signal()


def consumer(shared):
    """Function for the consumer to consume an object."""
    while True:
        shared.items.wait()
        if shared.finished:
            break
        shared.mutex.lock()
        sleep(randint(1, 10) / 100)
        shared.mutex.unlock()
        sleep(randint(1, 10) / 10)


def main():
    """Starts the experiment with 10 iterations for each settings
       to calculate the mean.
    """
    x = [100.0, 150.0, 200.0, 250.0, 300.0]
    y = [2.0, 4.0, 6.0, 8.0, 10.0]
    z = []
    xresults = []
    yresults = []
    zresults = []
    for ratio in x:
        for num_consumer in y:
            items_per_second_sum = 0
            for i in range(10):
                s = Shared(10)
                c = [Thread(consumer, s) for _ in range(2)]
                p = [Thread(producer, s, ratio)
                     for _ in range(int(num_consumer))]
                sleep(0.1)
                s.finished = True
                print(f"main thread {i}: waiting to finish")
                s.items.signal(100)
                s.free.signal(100)
                [t.join() for t in c + p]

                n_produced_items = s.counter
                items_per_second = n_produced_items / 0.1
                items_per_second_sum += items_per_second

                print(f"main thread {i}: finished")
                print(f'items per second: {items_per_second}')
                print(f'total count: {n_produced_items}')

            print(f'avg items per second: {items_per_second_sum / 10}')
            xresults.append(10/ratio)
            yresults.append(num_consumer)
            zresults.append(items_per_second_sum / 10)

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_xlabel('Production time')
    ax.set_ylabel('Number of manufacturers')
    ax.set_zlabel('Number of manufactured products per second')
    ax.plot_trisurf(
        xresults,
        yresults,
        zresults,
        cmap='viridis',
        edgecolor='none')
    plt.show()


if __name__ == "__main__":
    main()

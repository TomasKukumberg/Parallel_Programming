# :computer: Parallel programming and distributed systems
## Dining savages and cooks problem 🧑‍🍳
We have N number of savages, M number of portions and L number of cooks. The goal is to synchronize savages and cooks to continue eating and cooking when possible. 
## Analysis
We are using multiple synchronization patterns in this exercise:
1. Barrier
2. Semaphore
3. Event
4. Mutex

All these patterns are used for synchronization. For example, we are using the barrier to synchronize cooks. We wait until they are all finished, and only then we signalize to savages that the pot is full. Also, we use an Event to signalize all cooks that they can start cooking. Before I was using a semaphore for this as well, so i decided to change the strategy and the Event worked straight away. Event is also more appropriate for this, because we don't want only one cook to signalize he can cook, but we want to signalize all of them so they can simultaneously start working. Mutex is like always used to protect critical parts (shared memory). For example, in the barrier, we use a mutex to increase the counter.

## Pseudocode
Pseudocode is pretty straightforward, first one is the wait function in the barrier:
```python
def wait():
  mutex.lock()
  if number_of_waiters_equal_to_N():
    barrier.signal()
  mutex.unlock()
  barrier.wait()
```
savage function:
```python
def savage():
  while True:
    mutex.lock()
    if food_empty:
      signalize_to_cooks()
    mutex.unlock()
    eat()
```
cook function:
```python
def cook():
  while True:
    wait_for_empty_pot_signal()
    wait_for_barrier_access()
    only_one_cook_signal_to_savages()
```

## Experiments and results
So while solving this exercise, I've encountered 2 problems:
1. Deadlocks
2. Figuring out how to limit only one of the L cooks to signalize savages that pot is full

The first problem was easier to solve, it was just about understanding the problem and figuring out that we need Events, because we want to signalize all L of the cooks. The second problem was a bit harder. What we had to do was to use an additional boolean variable in the Shared class which represents the state if we already signalized to savages that the pot is full. If we did, the rest of the cooks will simply skip this signalization (and they will also correctly skip adding food to the pot, because there isn't any left). If we wouldn't use this variable, we would add food to the pot L times and that would be wrong. So this is why we used this variable, first to signalize only once, and to add the correct amount of food. 

We can see from the image that the eating always takes M times, which is the correct result:

![alt text](https://i.imgur.com/lBJTDdY.png)
## :scroll: Helpful links and resources i've used
1. [Our seminar and lectures](https://uim.fei.stuba.sk/predmet/i-ppds/)


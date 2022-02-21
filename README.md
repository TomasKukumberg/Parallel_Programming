# :computer: Parallel programming and distributed systems
## :one: First exercise
The main goal of this exercise is to understand how locks and concurrent programming works. We are supposed to start 2 new threads which both share a common index which points to the array. This is located in a structure called Shared in our program. 

Shared class consists of few attributes:
1. counter - this is the index that points to the array
2. end - this is a number which represents total number of entries in the array
3. elms - this is the array we are talking about

Shared class looks like this: 
```python
class Shared():
    def __init__(self, size):
        self.counter = 0
        self.end = size
        self.elms = [0] * size
```

All of them are shared between 2 threads and we are supposed to protect critical parts of the code with the use of locks (mutex) to make it work. 

### First approach (File 01.py)
The first and most simple example is to lock the whole function at the start and at the end:
```python
def increment(shared, mutex):
    mutex.lock()
    while shared.counter < shared.end:
        shared.elms[shared.counter] += 1
        shared.counter += 1
    mutex.unlock()
```

This way, the first thread will execute the whole function and correctly increments all elements of the array, first thread releases the lock so the 2nd thread starts running but immediately ends, because the condition in 'while' block is false. This way, we protected the critical part of the function where we increment the counter and also increment the value. We will end up with the correct number of 1's, although the second thread didn't do much. 
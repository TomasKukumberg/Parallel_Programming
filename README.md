# :computer: Parallel programming and distributed systems
## :one: First exercise
The main goal of this exercise is to understand how barriers and their specific implementations work - with the help of semaphores and events. Our task was to rework the solution, specifically to replace semaphores with events. The first solution was the easiest, because all we had to do was to replace the declaration of semaphore with the declaration of event. Also when we signal the other threads, we don't have to provide the number of threads we want to signalize as an arguments, because Events signalize all threads by default. Here is the wait function:

```python
    def wait(self):
        self.M.lock()
        self.C += 1
        if self.C == self.N:
            self.C = 0
            self.T.signal()
        self.M.unlock()
        self.T.wait()
```
We first lock because we want to safely increment the counter and compare if it's equal to number of threads, this is critical because it can happen at the 'same' time and it's a shared memory, that's why we need to lock it. If it's equal to N, we will signal other threads to continue.
## :two: Second exercise
Second exercise is similar to the first one, with the difference that the barrier is used in a loop. That's why we have to use two barriers. The second barrier is there to ensure that when the while loop repeats itself in the iteration, the calls don't race with each other, but wait instead. Here is the code of the wait function:
```python
    def wait(self):
        self.M.lock()
        self.C += 1
        if self.C == self.N:
            self.C = 0
            self.T.signal()
        self.M.unlock()
        self.T.wait()
        self.T.clear()
```
We also need to clear the event, if we want to use the same event again. We need to be very careful with the clear method, because if we clear before the wait function, we will get a deadlock.

# :computer: Parallel programming and distributed systems
## :one: First exercise (File 01.py)
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
## :two: Second exercise File 02.py)
Second exercise is similar to the first one, with the difference that the barrier is used in a loop. That's why we have to use two barriers. The second barrier is there to ensure that when the while loop repeats itself in the iteration, the calls don't race with each other, but wait instead. Here is the code where we use two barriers in the while loop to sync correctly:
```python
    while True:
        before_barrier(thread_id)
        b1.wait()
        after_barrier(thread_id)
        b2.wait()
```
We also need to clear the event, if we want to use the same event again. We need to be very careful with the clear method, because if we clear before the wait function, we will get a deadlock. Here is the wait function with the use of clear function:
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
## :three: Third exercise
I've tried this exercise, but couldn't come up with a solution. I think the correct approach would be to either use a barrier or a rendezvous pattern to synchronize i+1 and i thread together, and then calculate i+2. This approach would repeat until we get to the Nth result, which is the Nth Fibonacci's number we want to calculate.
## :notebook: Experiments and results
I've tested both solutions with the use of rand() functions to randomize thread switching of the scheduler. I've also used different thread sizes to make sure it's not just a coincidence that barrier works and all tests passed. All prints always printed N times the 'before' print and also N times 'after' print.
## :scroll: Helpful links and resources i've used
1. [Our seminar and lectures](https://uim.fei.stuba.sk/predmet/i-ppds/)
2. [This awesome video about mutex](https://youtu.be/oq29KUy29iQ)
3. [This awesome video about deadlocks](https://youtu.be/LjWug2tvSBU)

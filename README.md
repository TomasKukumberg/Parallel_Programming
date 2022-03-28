# :computer: Parallel programming and distributed systems
## Barber and customers problem 💇
We have N number of customers, one barber, and we want to implement a FIFO queue and also use concurrent programming to achieve getting haircuts in the order the customers (threads) came in. Barber is also a thread.
## Analysis
We are using multiple synchronization tools in this exercise:
1. Mutex
2. Semaphore

All these tools are used for synchronization. For example, we are using mutex to make sure queue operations are done only one at the time. Mutex for the queue is actually not needed, because this data structure is thread-safe by default. But i've still used mutex in the critical parts to showcase the possible dangers if queue wasn't thread safe. The second part where mutex is needed is when the customer is getting a haircut. Only one of the customers at the same time can get a haircut, because there is only one seat!


## Pseudocode
Customer function takes care of customer's new haircut, if he's already in the queue. He also needs to signal after customer is finished:
```python
def customer():
while True:  
  if in queue:
    wait_for_barber()
    get_haircut()
    signalFinished()
```
Barber function cuts customer's hair. He signals when he's done as well:
```python
def barber():
  while True:
    wait_for_customer()
    cutHair()
    signalFinished()
```
Enter shop function:
```python
def enterShop():
  if queue_not_full():
    get_in_queue()
  else:
    leave()
```

## Experiments and results
I've printed out all actions to the console to confirm customers are getting their hair cut in order and also if any customers leave, when the queue is full. That's why i've set up the space in barber shop to 3 to quickly fill up and see customers leaving:

![alt text](https://i.imgur.com/Cu2jZ7T.png)
## :scroll: Helpful links and resources i've used
1. [Our seminar and lectures](https://uim.fei.stuba.sk/predmet/i-ppds/)


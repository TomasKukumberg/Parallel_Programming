# :computer: Parallel programming and distributed systems
## Generators and scheduler 👨‍💻
We have N number of tasks (which are simple generators) and we want a scheduler to switch between them. We want the scheduler to decide which function will perform. We chose the most simple approach, and that is that the scheduler will switch between t1 and t2 fairly. 

## Our idea
What we want to do is to have functions odd, which will yield odd numbers, and function even, which will yield even numbers. We want to switch between these two tasks with a help of a scheduler. So the correct output in the end, if we start from 0, is 0,1,2...5...10. They must be in order from lowest to highest, because we want to achieve fair and regular switching of tasks with a help of the scheduler.

## Pseudocode
We first need the scheduler, which will control switching between task 1 and task 2:
```python
def scheduler(tasks):
  while tasks still not finished:  
    for t in tasks:
      continue_with_task()
```
We also need some task functions, in our example they're called odd and even. Both functions go like this:
```python
def task1():
  for i in 10:
    yield i
```
Task 2 is the same:
```python
def task1():
  for i in 10:
    yield i
```
## Explanation
But what really happens? Well, it's actually quite interesting. First we call the scheduler function with all tasks as an argument to the scheduler function. Then we try to call next on each task. If next is successfull, we will get the next yielded number. If not, we will get an StopIterationException and we will stop iterating all tasks and finish. But the important thing to notice is this: When we call next(f), the scheduler gives f function the main control, and only when this function yields a number, the control goes back to the scheduler. Now we do the same next call, but to the g function, like this: next(g). So now the main control is passed to the g function, the g function will go on until it encounters a yield, which will once again return the main control to the scheduler. This approach is enough to achieve a simple scheduler function, which will switch between these tasks.
## Experiments and results
I've printed out all actions to the console to confirm everything is working as expected.

![alt text](https://i.imgur.com/9PK5wZQ.png)
## :scroll: Helpful links and resources i've used
1. [Our seminar and lectures](https://uim.fei.stuba.sk/predmet/i-ppds/)
2. [This awesome article](https://www.pythonkitchen.com/python-generators-in-depth/)


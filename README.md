# :computer: Parallel programming and distributed systems
## Nvidia cuda 👨‍💻
We will want to use Nvidia GPU to perform our calculations. This is done by the library numba. We also use the library numpy for array manipulations.
We use 32 threads per block. We want to increment every element in the array by 50, so we shouuld get a 51 in each entry in the end.

## Experiments and results
Let's launch the program and make sure it increments correctly:
![alt text](https://i.imgur.com/jLYdq6l.png)

We can see each entry really is 51, because each element was initialized with a value of 1 and each thread incremented it by 50.

## :scroll: Helpful links and resources i've used
1. [Our seminar and lectures](https://uim.fei.stuba.sk/predmet/i-ppds/)



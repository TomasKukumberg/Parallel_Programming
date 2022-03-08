# :computer: Parallel programming and distributed systems
## The problem
The main problem we want to look at and solve is the question of consumers and producers. Let's say we have a storage where can we put and take away manufactured objects. But to manufacture a new object, we need to have a free space left in the storage. Also, if we want to consume an object, we need to have at least one object left in the storage. Furthermore, we need to synchronize different workers to not pick up the same object or to put a new object into the place at the same time.
## The solution
We can achieve this by using two semaphores, the first one will represent how much space is left in the storage (how many items we can still put there). The second semaphore represents how many items are currently in the storage. If there is none, we will wait and block the thread, until we signalize there's a new object we can consume. Similar analogy works for the first semaphore - if there's no space left, we will block the thread until we get a signal that there's space again and then put the new object there. I also need to mention the mutex locks, which will help us with the synchronization problem mentioned above in the first paragraph.
## Simulation
I need to note that I'm not using any kind of buffer, i'm just simulating the manufacture process by using a sleep function with a randomly generated number to simulate the process. That is because we don't actually care about producing actual things and we just want to model the synchronization part.
## Experiments and results
I'm testing different divisors for the sleep function to simulate different production time, i'm also testing different number of producers/consumers to see what kind of impact will it have on the number of manufactured products per second. I will show the results with the help of the matplot library, which helps me to visualize a 3D graph.
### :one: First experiment with different sized producers (File 01.py)
Logically, the more producers we have, the more products we should be making per second. That's exactly what's shown in the graph:

![alt text](https://i.imgur.com/58TWXfW.png)
![alt text](https://i.imgur.com/l9WDD5q.png)

### :two: Second experiment with different sized consumers (File 02.py)
Interesting thing happens here, and that's a situation where we produce more objects if we have more consumers. But why is that? Well, it's because if we have too few consumers, our producers will stop manufacturing new objects and they will be waiting until they can work again. So if we add more consumers, our producers will be able to produce more objects, thus our number of manufactured products per second will grow:

![alt text](https://i.imgur.com/rRX11Bl.png)


## :scroll: Helpful links and resources i've used
1. [Our seminar and lectures](https://uim.fei.stuba.sk/predmet/i-ppds/)
2. [Matplotlib documentation](https://matplotlib.org/2.0.2/mpl_toolkits/mplot3d/tutorial.html)

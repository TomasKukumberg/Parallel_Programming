# :computer: Parallel programming and distributed systems
## Async programming in Python with asyncio 👨‍💻
I chose the typical problem which is used when explaining the benefits of async programming and that is the example of playing chess. Let's say we have Judit which takes 1 second to make a turn, and an average player that takes 5 seconds to make a turn (unrealistic times to make the program run faster).
Let's say an average game takes 12 rounds. Let's also have 4 opponents to Judit, so there will be 4 games played in total. Now let's calculate how long would it take to finish all of these games in a traditional, sync way:

(JUDIT_TURN_TIME + AVG_PLAYER_TIME) * AVG_ROUNDS * OPPONENTS

which in our case translates to:

(1 + 5) * 12 * 4 = 288 seconds.

Now that's a lot of time. But what if Judit could asynchronously play on each board? She doesn't have to wait for each player to make a turn, but she can move to the next table and make a turn. This would save us a lot of time! Let's calculate how long would this improved version of playing take:

(1+5) * 12 = 72 seconds.

That's 4 times less! That's a big difference. Now we will show some code and later also do some proper testing to show our theory works.
 

## Pseudocode
We need a loop that will perform all rounds and moves by the players, asynchronously:
```python
for i in AVG_ROUNDS:
  judit_move()
  avg_player_move()
```

## Experiments and results
Let's measure the time and see for ourselves that our calculations are correct:

Sync way:

![alt text](https://i.imgur.com/875BF3k.png)

Async way:

![alt text](https://i.imgur.com/1a3eCyR.png)

From the screens we can see our function runs much faster with the async method and also that are calculations are correct.

## :scroll: Helpful links and resources i've used
1. [Our seminar and lectures](https://uim.fei.stuba.sk/predmet/i-ppds/)
2. [This awesome article](https://realpython.com/async-io-python/#the-10000-foot-view-of-async-io)



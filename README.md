# :computer: Parallel programming and distributed systems
## Nuclear factory problem
We have 8 different monitors and 3 different sensors. Sensors are sending data to the data source in a time cycle and monitors are checking if there's new data available in a data source in a time cycle as well. Our goal is to implement a communication between these two in a best way possible.
## Analysis
We are using multiple synchronization patterns in this exercise:
1. Turnstile
2. Semaphore for data source control
3. Two Lightswitches (for monitors and sensors)
4. Events for signalization

All these patterns are used for synchronization. For example, we are using our own class called ValidData, which signalizes with an Event to let monitors know they can start working (because all 3 sensors updated the values). Turnstile is used to release all sensors before monitors start to access the critical part with data. After we are done updating the data, we unlock the turnstile.

## Pseudocode
Pseudocode is pretty straightforward, first one is the monitor function:
```python
fun monitor():
  dont_start_until_3_sensors_ready()
  while True:
    delay()
    lock_turnstile()
    do_work()
    unlock_turnstile()
```
cidlo function:
```python
fun sensors():
  sensors_passing_until_monitor_locks_turnstile()
  get_access_to_data_and_lock_lightswitch()
  do_work()
  signal_if_all_sensors_wrote_atleast_once()
  unlock_lightswitch()
```
## Experiments and results
We could decide where we place the line in cidlo function, either this:
```python
def cidlo(cidlo_id, turniket, ls_cidlo, valid_data, access_data):
    """
    Sensors are passing through the turnstile until monitor locks it
    """
    while True:
        sleep(randint(50, 60) / 1000)
        turniket.wait()
        pocet_zapisujucich_cidiel = ls_cidlo.lock(access_data)
        turniket.signal()

        if cidlo_id == 1 or cidlo_id == 2:
            trvanie_zapisu = randint(10, 20) / 1000
        else:
            trvanie_zapisu = randint(20, 25) / 1000
        print(f'cidlo "{cidlo_id:02d}":  '
              f'pocet_zapisujucich_cidiel={pocet_zapisujucich_cidiel:02d}, '
              f'trvanie_zapisu={trvanie_zapisu:5.3f}')
        sleep(trvanie_zapisu)
        valid_data.try_signal()
        ls_cidlo.unlock(access_data)
```
or this:
```python
def cidlo(cidlo_id, turniket, ls_cidlo, valid_data, access_data):
    """
    Sensors are passing through the turnstile until monitor locks it
    """
    while True:
        sleep(randint(50, 60) / 1000)
        turniket.wait()
        turniket.signal()
        pocet_zapisujucich_cidiel = ls_cidlo.lock(access_data)

        if cidlo_id == 1 or cidlo_id == 2:
            trvanie_zapisu = randint(10, 20) / 1000
        else:
            trvanie_zapisu = randint(20, 25) / 1000
        print(f'cidlo "{cidlo_id:02d}":  '
              f'pocet_zapisujucich_cidiel={pocet_zapisujucich_cidiel:02d}, '
              f'trvanie_zapisu={trvanie_zapisu:5.3f}')
        sleep(trvanie_zapisu)
        valid_data.try_signal()
        ls_cidlo.unlock(access_data)
```
It just depends if we want to prioritize monitors over sensors, or vice versa. I've chosen the first option.
![alt text](https://i.imgur.com/oM5ssP8.png)
## :scroll: Helpful links and resources i've used
1. [Our seminar and lectures](https://uim.fei.stuba.sk/predmet/i-ppds/)
2. [Matplotlib documentation](https://matplotlib.org/2.0.2/mpl_toolkits/mplot3d/tutorial.html)


"""
Copyright 2022 Tomas Kukumberg <tomas.kukumberg@centrum.sk>
This code is licensed under MIT license
This module is dealing with the 'playing chess in a synchronized way' problem.
"""

import time

AVG_ROUNDS = 12
JUDIT_TIME = 1
PLAYER_TIME = 5
OPONENTS = 4


def chess():
    for i in range(AVG_ROUNDS):
        print("Judit move")
        time.sleep(JUDIT_TIME)
        print('Player move')
        time.sleep(PLAYER_TIME)
        print("Two")


def main():
    for i in range(OPONENTS):
        chess()

if __name__ == "__main__":
    s = time.perf_counter()
    main()
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

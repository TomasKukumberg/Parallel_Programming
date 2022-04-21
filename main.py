"""
Copyright 2022 Tomas Kukumberg <tomas.kukumberg@centrum.sk>
This code is licensed under MIT license
This module is dealing with the 'playing chess in async way' problem.
"""

import asyncio
import time

AVG_ROUNDS = 12
JUDIT_TIME = 1
PLAYER_TIME = 5
OPONENTS = 4


async def chess():
    """Function to play chess (async)"""
    for i in range(AVG_ROUNDS):
        print("Judit move")
        await asyncio.sleep(JUDIT_TIME)
        print('Player move')
        await asyncio.sleep(PLAYER_TIME)
        print("Two")


async def main():
    """Main function"""
    await asyncio.gather(chess(), chess(), chess(), chess())

if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")

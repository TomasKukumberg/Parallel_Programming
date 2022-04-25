"""
Copyright 2022 Tomas Kukumberg <tomas.kukumberg@centrum.sk>
This code is licensed under MIT license
This module is dealing with Nvidia GPU computing problem.
"""

from numba import cuda
import numpy
from fei.ppds import print


@cuda.jit
def my_kernel(data):
    """Function that increments each element in the array by 50."""
    pos = cuda.grid(1)
    if pos < data.size:
        data[pos] += 50


SIZE = 122

data = numpy.ones(SIZE)

THREADS_PER_BLOCK = 32
BLOCKS_PER_GRID = (data.size + (THREADS_PER_BLOCK - 1)) // THREADS_PER_BLOCK


my_kernel[BLOCKS_PER_GRID, THREADS_PER_BLOCK](data)
print(data)

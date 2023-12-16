import functools


@functools.cache
def cached_function(i):
    print(i)
    return 1

for i in range(100):
    cached_function(10)
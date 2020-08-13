import time
import functools
from timing_tutorial import TimerDC
from Timer import Timer_class
import timeit
import gc

def my_timer(func, *args):
    start = time.perf_counter()
    func.__call__(*args)
    stop = time.perf_counter()
    duration = stop - start
    return duration

def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(F"Elapsed time: {elapsed_time:0.6f} seconds")
        return value
    return wrapper_timer

# ====================
# Fibonacci Functions:
# ====================

# A very bad implementation of fibonacci calculator
# it can be massively improved by using functools.lru_cache decorator
# @Timer_class.Timer()
def fib1(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return (fib1(n-2) + fib1(n-1))

# A slightly better implementation of fibonacci calculator:
# @Timer_class.Timer(number=5)
def fib2(n):
    def aux(v1, v2, n, v):
        if n == 0:
            return v
        elif n == 1:
            return v
        else:
            n -= 1
            v = v1 + v2
            v1 = v2
            v2 = v
            return aux(v1, v2, n, v)
    
    return aux(0,1,n,0)

@Timer_class.Timer(number=5)
def func1(n):
    return fib1(n)

@Timer_class.Timer(number=5)
def func2(n):
    return fib2(n)

#print(fib1(40))
#print(my_timer(fib1, 30)*1000000.0, " microseconds")
#print(my_timer(fib2, 30)* 1e06, " microseconds")
#print(fib2(40))



@Timer_class.Timer()
def main():
    # fib1_time = timeit.timeit(stmt="fib1(30)", setup="from timing import fib1", number=1)
    # fib2_time = timeit.timeit(stmt="fib2(30)", setup="from timing import fib2", number=1)
    # print(f"fib1 took {fib1_time:0.6f}")
    # print(f"fib2 took {fib2_time:0.6f}")

    # with Timer_class.Timer():
    #     fib1(30)
    # print(func1(30))
    # print(func2(30))
    
    # print("Elapsed time: {:0.6f} seconds".format(timing))
    fib1(30)
    fib2(30)
    print(fib1(30))
    print(fib2(30))
    
    
    


if __name__ == "__main__":
    main()
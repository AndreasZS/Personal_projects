import time

# Accepts function as a parameter
def func(f):
    # wrapper needs the same number of arguments as function f
    def wrapper(*args, **kwargs): # Now accepts any number of arguments or keyword arguments
        print("Started")
        f(*args, **kwargs) # Calls function that was passed in 
        print("Ended")
        # to return values add 2 lines, rv = f(*args, **kwargs) and return rv, to wrapper def
    return wrapper # returns function

@func
def func2(x, y):
    print(x)
    return y

@func # Put @ sign and name of decorated function, equivalent to func3 = func(func3) 
def func3():
    print("i am func3")



x = func2(5, 6)
print(x)

# Good uses for decorators: checking input is valid, timing code, logging execution
# Timer decorator
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        rv = func()
        total = time.time() - start
        print("Time:", total)
        return rv

    return wrapper

@timer
def test():
    for _ in range(100000):
        pass

@timer
def test2():
    time.sleep(2)

test()
test2()
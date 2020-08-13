import time
from dataclasses import dataclass, field
from typing import Any, Callable, ClassVar, Dict, Optional
import functools
from contextlib import ContextDecorator

class TimerError(Exception):
    """Custom exception to report errors"""

# ===============================
# Regular implementation of Timer
# ===============================
class Timer:
    def __init__(self, text="Elapsed time: {:0.4f} seconds", logger=print):
        # to use f-string for .text you need double curly braces:
        # f"Finished {task} in {{:0.4f}} seconds"
        self._start_time   = None
        self.text          = text   # Output text
        self.logger        = logger # Function that takes string argument to log output
        self._elapsed_time = 0

    def start(self):
        """Start new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")
        self._start_time = time.perf_counter()

    def pause(self):
        """Stop timer but do not report time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")
        self._pause_time = time.perf_counter()
        self._elapsed_time += self._pause_time - self._start_time
        self._start_time = self._pause_time

    def stop(self):
        """Stop timer, report elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        self._elapsed_time += time.perf_counter() - self._start_time
        self._start_time = None
        
        if self.logger:
            self.logger(self.text.format(self._elapsed_time))
        #print(self.text.format(self._elapsed_time))
        return self._elapsed_time




# =================================
# Dataclass implementation of Timertutorial = feed.get_article(0)
# =================================
"""Timer is made into a dataclass using the @dataclass decorator.
   To use a data class, variables must be annotated. This allows type hints to be added.
   If you do not want to use type hints you can annotate all variables with 'Any'"""
@dataclass
class TimerDC(ContextDecorator):
    timers: ClassVar[Dict[str, float]] = dict() # ClassVar annotation tells data classes that .timers is a class variable, dictionary of timers
    name: Optional[str] = None                  # Attribute on TimerDC, can be defined when creating Timer instance, default is None
    text: str = "Elapsed time: {:0.6f} seconds" # Attribute on TimerDC
    logger: Optional[Callable[[str], None]] = print # Attribute on TimerDC
    _start_time: Optional[float] = field(default=None, init=False, repr=False) # dataclasses.field() says that start time should be removed from .__init__() and the repr of Timer, we want it hidden

    # .__post_init__() is used for any initialization that is not apart of setting instance attributes
    # here we use it to add named timers to .timers
    def __post_init__(self) -> None:
        """Add timer to dict of timers after initialization"""
        if self.name:
            self.timers.setdefault(self.name, 0)
    
    def start(self) -> None:
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")
        self._start_time = time.perf_counter()

    def stop(self) -> float:
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")
        
        # Calculate elapsed time
        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        
        # Report elapsed time
        if self.logger:
            self.logger(self.text.format(elapsed_time))
        if self.name:
            self.timers[self.name] += elapsed_time
        
        return elapsed_time
    

    
    # Next step is to add a context manager
    """Currently to use the Timer class we need to:
        1. Instantiate the class
        2. Call .start() before the code block we want to time
        3. Call .stop() after the code block we want to time
    
        A context manager can be used to call functions before and after a block of code."""
    # Context Manager example:
    # with EXPRESSION as VARIABLE:
    #     BLOCK
    """ 
    EXPRESSION returns a context manager which is optionally bound to the name VARIABLE.
    BLOCK is any regular Python code block. Context managers are most commonly used to handle
    resources like files, locks, and database connections. They free and clean up the resource
    after it has been used.
        Context manager protocol consists of two methods:
        .__enter__(self) when entering relative context
        .__exit__(self, type, value, traceback) when exiting relative context
        so to create your own context manager you need to implement these methods.
        .__exit__() can be used to handle exceptions. After properly handling exception you should return True.
    You can also use the contextmanager decorator from contextlib to turn a generator into a contextmanager.
    """

    def __enter__(self) -> "Timer":
        """Start a new timer as a context manager"""
        self.start()
        return self

    def __exit__(self, *exc_info: Any) -> None:
        """Stop the context manager timer"""
        self.stop()
    
    # Now to use Timer() as a context manager:
    # with Timer():
    #     'code block'
    """We no longer need an extraneous varialbe for the class instantiation.
       However, to use the context manager we either have to use Timer every time we call a function (see above)
       or wrap the function body inside a context manager. 
       def do_something():
           with Timer("some_name"):
       
       instead we can use Timer as a decorator."""
  
    # Next step is to use Timer as a decorator. 
    """ Decorators modify the behavior of functions and classes
        This is possible since functions are first-class objects in Python
        
        functools.wraps preserves metadata of decorated function
        Should be used whenever you define a decorator """

    # __call__() not needed when interiting from ContextDecorator
    """ def __call__(self, func):
            '''Support using Timer as a decorator'''
            @functools.wraps(func)
            def wrapper_timer(*args, **kwargs):
                with self:
                    return func(*args, **kwargs)
            
            return wrapper_timer """

# ========================
# Basic Decorator Template
# ========================
def decorator(func):
    @functools.wraps(func)
    def wrapper_decorator(*args, **kwargs):
        # Do something before
        value = func(*args, **kwargs)
        # Do something after
        return value
    return wrapper_decorator

# =====================
# Basic Timer Decorator
# =====================
def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        tic = time.perf_counter()
        value = func(*args, **kwargs)
        toc = time.perf_counter()
        elapsed_time = toc - tic
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")
        return value
    return wrapper_timer

# Apply the decorator like this:
"""
@timer
def latest_tutorial():
    tutorial = feed.get_article(0)
    print(tutorial)
"""
# Or if the function has already been defined. 
# feed.get_article = timer(feed.get_article)
# (You only need to apply the decorator once)

# Application of improved Timer decorator
"""
@Timer(text="Downloaded the tutorial in {:.2f} seconds")
def latest_tutorial():
    tutorial = feed.get_article(0)
    print(tutorial)
"""

# Context managers and Decorators have some similarities
# There is a class defined in contextlib called 'ContextDecorator'
# Decorator abilities can be added to context manager classes by inheriting ContextDecorator
# e.g. class Timer(ContextDecorator):
# Note. there is NO need to implement .__call__() yourself
# It is just syntactic sugar for any construct of the form:
# def f():
#     with cm():
#
# You can instead write:
# @cm()

"""
Note: Decorated function must be able to be called multiple times,
      the underlying context manager must support use in multiple
      'with' statements. If this is not the case then use the original
      construct with the explicit 'with' statement inside the function."""

""" 
Summation: timer can be used as class, context manager, or decorator
for small code snippets try the 'timeit' standard library
iPython shell and Jupyter notebook have a %timeit command
for larger code you can use a profiler like cProfile. 

command line example:
python -m cProfile -o latest_tutorial.prof latest_tutorial.py

runs the .py file with profiling turned on. Saves the output in binary
format to the .prof file. 
You can then use pstats to open an interactive profile statistics browser.
python -m pstats latest_tutorial.prof

then type commands into command prompt like help, strip, sort, stats
Profiling can help get an idea of where code is spending most of its time. 
From there you can try to optimize bottlenecks.

line_profiler can be used to see which lines in a function are the slowest.
However, line profiling takes time and is not part of the standard library.
To tell it which functions to profile you add a profile decorator to the function.
then run the profiler using kernprof, results are saved to .lprof file, 
see results using 'python -m line_profiler filename.lprof'
"""


# Look into:
# Making Timer decorator keep track of whether it's executing top level of recursion or not and only print info for top level, uses 'nonlocal' directive
# Also 'lru_cache' from functools, keeps cache of recently computed resuts so they don't need to be re-computed. 

"""
def rclock(func):
    top = True
    @wraps(func)
    def clocked(*args):
        nonlocal top
        if top:
            top = False
            t0 = time.perf_counter()
            result = func(*args)
            elapsed = time.perf_counter() - t0
            name = func.__name__
            arg_str = ', '.join(repr(arg) for arg in args)
            print('[%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        else:
            result = func(*args)
            top = True
        return result
    return clocked
"""

"""decorator syntax:
@deco
def func(arg1, arg2, ...):
    pass

is same as

def func(arg1, arg2, ...):
    pass
func = dec(func)
"""
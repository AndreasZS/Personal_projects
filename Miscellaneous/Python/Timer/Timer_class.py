import time
from dataclasses import dataclass, field
from typing import Any, Callable, ClassVar, Dict, List, Optional
import functools
from contextlib import ContextDecorator

"""
-This is mostly adapted from code found here: https://realpython.com/python-timer/#a-python-timer-context-manager
-This was run using Python 3.8.0 on Linux Ubuntu 18.04.5 
-Currently this Timer class cannot decorate recursive functions on their own.
 You either have to call the recursive function within a function or
 use Timer as a context manager in a 'with' statement where the body is the function call you want to time
-For this reason the decorator is best used on a 'main()' function that contains function calls you wish to time
"""

class TimerError(Exception):
    """Custom exception to report errors"""

# ========================================
# ContextDecorator implementation of Timer
# ========================================
@dataclass
class Timer(ContextDecorator):
    name:          Optional[str]   = None                                        # Name of function being timed, can be used for dictionary purposes
    text:          str             = "Elapsed time: {:0.6f} seconds"             # Text used when logging elapsed time
    logger:        Optional[Callable[[str], None]] = print                       # Logging function, default is print()
    number:        Optional[int]   = 1                                           # Number of times to repeat function execution
    trace:         Optional[bool]  = False                                       # Boolean value, if true then traceback will be printed
    _time_array:   ClassVar[List[str]] = []                                      # Array of times used when number is greater than 1
    _start_time:   Optional[float] = field(default=None, init=False, repr=False) # Start time of timer
    _stop_time:    Optional[float] = field(default=None, init=False, repr=False) # Stop time of timer
    _elapsed_time: Optional[float] = field(default=0.0, init=False, repr=False)  # Elapsed time of timer
    
    def __post_init__(self) -> None:
        self._time_array = []
    
    def start(self) -> None:
        """Start a new timer"""
        # Check if timer is currently running
        if self._start_time != None:
                raise TimerError(f"Timer is running, use .stop() to stop it.")
        # Otherwise start a timer
        self._start_time = time.perf_counter() 
    
    def pause(self) -> None:
        """Pause a timer"""
        if self._start_time == None:
            raise TimerError(f"Timer is not running, use .start() to start it.")
        self._pause_time = time.perf_counter()

    def stop(self) -> float:
        """Stop the timer and calculate the elapsed time"""
        # Check if timer is currently running
        if self._start_time == None:
            raise TimerError(f"Timer is not running, use .start() to start it.")
        # Stop timer and calculate elapsed time
        self._stop_time = time.perf_counter()
        self._elapsed_time = self._stop_time - self._start_time
        # Add elapsedtime to array of times
        f_elapsed = f"{self._elapsed_time:0.6f}"
        self._time_array.append(f_elapsed)
        # Reset start time to None
        self._start_time = None
        return self._elapsed_time
    
    def log(self) -> None:
        """Calls self.logger to log the results of timing."""
        min_time = float(min(self._time_array))
        if self.logger:
            # self.logger(self.text.format(self._elapsed_time))
            self.logger(self.text.format(min_time))
        # if self.name:
        #     self.timers[self.name] += self._elapsed_time
        if len(self._time_array) == self.number and self.number > 1:
            print(self._time_array)
        
    # Context Manager methods:
    def __enter__(self) -> "Timer":
        '''Enter runtime context of object: Start a new timer as a context manager'''
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        '''Exit runtime context of object: Stop the context manager timer.
           Parameters describe exception that caused exit. If no exception then all 3 arguments are None.'''

        # Stop the timer
        self.stop()
        # If function has been timed for 'self.number' executions then we are done, log it
        if len(self._time_array) == self.number or self.number == 1:
            self.log()
        # If trace is set to true then print type, value, and traceback
        if self.trace:
            print(f"type: {exc_type}, value: {exc_value}, trace: {traceback}")
        
    
    # Makes this class a 'Callable' which is needed in order to use it as a decorator, technically not needed since it inherits from 'ContextDecorator'
    def __call__(self, func):
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            # Loop to execute 'self.number' time trials
            # self._time_array = []
            for x in range(self.number):   
                with self:        
                    result = func(*args, **kwargs)
                    # func(*args, **kwargs)
                    # return func(*args, **kwargs)
            return result
            # return func(*args, **kwargs)
        return wrapper_timer
   

# This decorator works as a timer if there is only one recursive call in the return statement
def RecTimer(func):
        top = True
        @functools.wraps(func)
        def wrapper_timer(*args, **kwargs):
            nonlocal top
            if top:
                top = False
                t0 = time.perf_counter()
                result = func(*args, **kwargs)
                elapsed = time.perf_counter() - t0
                print("Elapsed time: {:0.6f} seconds".format(elapsed))
            else:
                result = func(*args, **kwargs)
                top = True
            return result
        
        return wrapper_timer









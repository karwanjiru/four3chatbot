import time
import replicate


def debounce(func, wait):
    last_called = 0
    
    def debounced(*args, **kwargs):
        nonlocal last_called
        now = time.time()
        elapsed = now - last_called
        
        if elapsed < wait:
            # If called too soon, reset the timer
            last_called = now
        else:
            # If called after the debounce period, execute the function
            last_called = now
            return func(*args, **kwargs)
    
    return debounced
# Import the time module, which provides functions for working with time and dates
import time

# Import the replicate module, which is likely a custom module for interacting with a replicate API
import replicate

# Define a function called debounce, which takes a single argument 'wait'
def debounce(wait):
    # Define a decorator function called decorator, which takes a function 'fn' as an argument
    def decorator(fn):
        # Define a new function called debounced, which will wrap the original function 'fn'
        def debounced(*args, **kwargs):
            # Check if the debounced function has an attribute called '_last_call_time'
            # This attribute will store the timestamp of the last time the function was called
            if hasattr(debounced, '_last_call_time') and time.time() - debounced._last_call_time < wait:
                # If the time since the last call is less than the 'wait' period, return immediately
                # This is the debouncing mechanism, which prevents the function from being called too frequently
                return
            # Update the '_last_call_time' attribute with the current timestamp
            debounced._last_call_time = time.time()
            # Call the original function 'fn' with the provided arguments and keyword arguments
            return fn(*args, **kwargs)
        # Return the debounced function
        return debounced
    # Return the decorator function
    return decorator

# Use the debounce decorator to wrap the replicate_run function
# The debounce time is set to 0.5 seconds, which means the function will not be called more frequently than once every 0.5 seconds
@debounce(0.5)  # Adjust the debounce time as needed
def replicate_run(model, input_params):
    # Call the replicate.run function with the provided model and input parameters
    return replicate.run(model, input=input_params)
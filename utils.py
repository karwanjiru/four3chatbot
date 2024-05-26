import time
import replicate

def debounce(wait):
    def decorator(fn):
        def debounced(*args, **kwargs):
            if hasattr(debounced, '_last_call_time') and time.time() - debounced._last_call_time < wait:
                return
            debounced._last_call_time = time.time()
            return fn(*args, **kwargs)
        return debounced
    return decorator

@debounce(0.5)  # Adjust the debounce time as needed
def replicate_run(model, input_params):
    return replicate.run(model, input=input_params)

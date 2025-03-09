import functools

def squeak(func):
    @functools.wraps(func)
    def wrapper_SQUEAK(*args, **kwargs):
        print("SQUEAK")
        return func(*args, **kwargs)
    return wrapper_SQUEAK
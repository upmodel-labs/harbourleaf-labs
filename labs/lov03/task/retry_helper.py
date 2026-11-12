"""The supplied suite's retry helper (step 4). It re-runs a failing test up to `times` times.

Real tests that call a live model or tool get fresh randomness on every attempt, so a retry
can turn a red test green. Here the test draws a new seed on each attempt to behave the same way.
"""
import functools


def retry_on_failure(times=3):
    def decorate(test):
        @functools.wraps(test)
        def wrapper(*args, **kwargs):
            last = None
            for _ in range(times):
                try:
                    return test(*args, **kwargs)
                except AssertionError as error:
                    last = error
            raise last
        return wrapper
    return decorate

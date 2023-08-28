import time
from functools import wraps
from typing import Any, Callable, Generator, Iterable, TypeVar

from sleep_funcs import SleepCallable, full_jitter

WrappedFuncReturnType = TypeVar('WrappedFuncReturnType')


def isinstance_in_iterable(instance: Any, types: Iterable[type[Any]]) -> Generator[bool, None, None]:
    yield from (isinstance(instance, instance_type) for instance_type in types)


def backoff(
    start_sleep_time: float = 0.1,
    factor: float = 2,
    border_sleep_time: float = 10,
    sleep_func: SleepCallable = full_jitter,
    exceptions_that_support_attempts: Iterable[type[Exception]] = (Exception,),
) -> Callable[[Callable[..., WrappedFuncReturnType]], Callable[..., WrappedFuncReturnType]]:
    def func_wrapper(func: Callable[..., WrappedFuncReturnType]) -> Callable[..., WrappedFuncReturnType]:
        @wraps(func)
        def inner(*args: Any, **kwargs: Any) -> WrappedFuncReturnType:
            attempt = 0
            sleep = start_sleep_time
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as exception:
                    must_raise: bool = not any(isinstance_in_iterable(exception, exceptions_that_support_attempts))
                    if must_raise:
                        raise exception
                    sleep = sleep_func(
                        start_sleep_time=start_sleep_time,
                        factor=factor,
                        border_sleep_time=border_sleep_time,
                        attempt=float(attempt),
                        previous_sleep_time=sleep,
                    )
                    time.sleep(sleep)

                attempt += 1

        return inner

    return func_wrapper

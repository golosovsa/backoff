from random import random
from typing import Protocol


class SleepCallable(Protocol):
    def __call__(self, **kwargs: float) -> float: ...


def no_jitter(**kwargs: float) -> float:
    border_sleep_time: float = kwargs['border_sleep_time']
    start_sleep_time: float = kwargs['start_sleep_time']
    factor: float = kwargs['factor']
    attempt: float = kwargs['attempt']
    delay: float = min(border_sleep_time, start_sleep_time * factor ** attempt)
    return delay


def full_jitter(**kwargs: float) -> float:
    border_sleep_time: float = kwargs['border_sleep_time']
    start_sleep_time: float = kwargs['start_sleep_time']
    factor: float = kwargs['factor']
    attempt: float = kwargs['attempt']
    half_delay = no_jitter(
        border_sleep_time=border_sleep_time,
        start_sleep_time=start_sleep_time,
        factor=factor,
        attempt=attempt,
    ) / 2
    delay: float = half_delay + random() * half_delay
    return delay


def equal_jitter(**kwargs: float) -> float:
    border_sleep_time: float = kwargs['border_sleep_time']
    start_sleep_time: float = kwargs['start_sleep_time']
    previous_sleep_time: float = kwargs['previous_sleep_time']
    return min(border_sleep_time, random() * abs(previous_sleep_time * 3 - start_sleep_time))

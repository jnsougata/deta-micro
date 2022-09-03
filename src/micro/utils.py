import inspect


def single_arged(func) -> bool:
    return len(inspect.getfullargspec(func).args) == 1


def coro(func) -> bool:
    return inspect.iscoroutinefunction(func)

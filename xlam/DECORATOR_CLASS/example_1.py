from functools import wraps
from typing import Callable

from icecream import ic


def decor(f):
    @wraps(f)
    def wr(*args, **kwargs):
        ic(f.__name__, *args, **kwargs)
        result = f(f, *args, **kwargs)
        ic(result)
        return result

    return wr


def decorator(func: "Example"):
    def wrapper(*args, **kwargs):
        ic("decorator ready", func)
        for key, item in func.__dict__.items():
            if not key.startswith("_") and isinstance(item, Callable):
                ic(
                    key,
                    item,
                )
                setattr(func, key, decor(item)(*args, **kwargs))
        return func(*args, **kwargs)  # noqa

    return wrapper


@decorator
class Example:
    def __init__(self):
        self.x = 0

    def foo(self):
        self.x += 1
        return self.x

    def bar(self):
        self.x -= 1
        return self.x

    def __str__(self):
        ic(111111)
        return self.__class__.__name__

    __repr__ = __str__


if __name__ == "__main__":
    # ic("Start program")
    ex = Example()
    # ic()
    ic(ex.foo())
    ic(ex.bar())
    ic(ex.foo())
#


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class CustomFormatter(logging.Formatter):
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS = {
        logging.DEBUG: grey + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

from functools import wraps
from datetime import datetime


def timing(logger, filename=None):
    def with_logger(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            ret = func(*args, **kwargs)
            logger.info(
                f"{filename or '-'}: {func.__name__} executed in {(datetime.now() - start_time).seconds}s")
            return ret

        return wrapper

    return with_logger

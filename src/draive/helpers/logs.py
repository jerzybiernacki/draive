from logging.config import dictConfig

from draive.helpers.env import getenv_bool

__all__ = [
    "setup_logging",
]


# NOTE: this function should be run only once on application start
def setup_logging(
    *__names: str,
    debug: bool = getenv_bool("DEBUG_LOGGING", __debug__),
):
    dictConfig(
        config={
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "standard": {
                    "format": "%(asctime)s [%(levelname)-4s] [%(name)s] %(message)s",
                    "datefmt": "%d/%b/%Y:%H:%M:%S +0000",
                },
            },
            "handlers": {
                "console": {
                    "level": "DEBUG" if debug else "INFO",
                    "formatter": "standard",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                "": {  # root logger
                    "handlers": ["console"],
                    "level": "DEBUG" if debug else "INFO",
                    "propagate": False,
                },
                **{
                    name: {
                        "handlers": ["console"],
                        "level": "DEBUG" if debug else "INFO",
                        "propagate": False,
                    }
                    for name in __names
                },
            },
        },
    )

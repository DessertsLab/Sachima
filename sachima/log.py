import logging
import logging.config
import sys
from sachima import conf


LOGGING_CONFIG_DEFAULTS = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        "sachima.root": {"level": "INFO", "handlers": ["console"]},
        "sachima.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            "propagate": True,
            "qualname": "sachima.error",
        },
    },
    handlers={
        "console": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "generic",
            "filename": conf.get("LOG_DIR") + "/sachima.log",  # noqa
            "maxBytes": 1024000,
            "backupCount": 10,
            # "stream": sys.stdout,
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stderr,
        },
    },
    formatters={
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        }
    },
)

logging.config.dictConfig(LOGGING_CONFIG_DEFAULTS)
logger = logging.getLogger("sachima.root")
logger.setLevel(conf.get("LOG_LEVEL"))

import logging
import logging.config
import sys
from sachima import conf
from tqdm import tqdm


class DummyTqdmFile(object):
    """ Dummy file-like that will write to tqdm
    https://github.com/tqdm/tqdm/issues/313
    """

    file = None

    def __init__(self, file):
        self.file = file

    def write(self, x):
        # Avoid print() second call (useless \n)
        # if len(x.rstrip()) > 0:
        tqdm.write(x)
        # self.buf = buf.strip("\r\n\t ")

    def flush(self):
        return getattr(self.file, "flush", lambda: None)()


LOGGING_CONFIG_DEFAULTS = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        "sachima.root": {"level": "INFO", "handlers": ["file", "console"]},
        "sachima.error": {
            "level": "INFO",
            "handlers": ["error_console"],
            "propagate": True,
            "qualname": "sachima.error",
        },
    },
    handlers={
        "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "generic",
            "filename": conf.get("LOG_DIR") + "/sachima.log",  # noqa
            "maxBytes": 1024000,
            "backupCount": 10,
            # "stream": sys.stdout,
        },
        # "console1": {
        #     "class": "logging.StreamHandler",
        #     "formatter": "generic",
        #     "level": "DEBUG",
        # },
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "level": "DEBUG",
            "stream": DummyTqdmFile(sys.stderr),
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stderr,
        },
    },
    formatters={
        "generic": {
            "format": "%(asctime)s [%(process)d] [%(processName)s] [%(levelname)s] %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter",
        }
    },
)

logging.config.dictConfig(LOGGING_CONFIG_DEFAULTS)
logger = logging.getLogger("sachima.root")
logger.setLevel(conf.get("LOG_LEVEL"))

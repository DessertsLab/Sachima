import sys
import os
import logging
sys.path.insert(0, os.getcwd())

# from sachima.log import logger


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJ_DIR = "./"

# ---------------------------------------------------------
# Superset API
# ---------------------------------------------------------
SUPERSET_WEBSERVER_ADDRESS = "http://0.0.0.0/"
SUPERSET_WEBSERVER_PORT = 8088
SUPERSET_USERNAME = "admin"
SUPERSET_PASSWORD = "general"
SUPERSET_API_TABLE_BP = "/sachima/v1/save_or_overwrite_slice/"

# ---------------------------------------------------------
# mail config
# ---------------------------------------------------------
MAIL_HOST = ""
MAIL_ADD = ""
MAIL_USER = ""
MAIL_PASS = ""
MAIL_SENDER = "MAIL_SENDER"

# ---------------------------------------------------------
# sns config
# ---------------------------------------------------------
SNS_DINGDING_ERROR_GRP_TOKEN = ""
SNS_DINGDING_INFO_GRP_TOKEN = ""
SNS_DINGDING_SENDING_STR = ""
SNS_DINGDING_ERRSENT_STR = ""

# ---------------------------------------------------------
# db config
# ---------------------------------------------------------
DB_SUPERSET = "~/.superset/superset.db"

# ---------------------------------------------------------
# logging config
# ---------------------------------------------------------
LOG_LEVEL = logging.DEBUG
LOG_DIR = PROJ_DIR + "/logs"

# ---------------------------------------------------------
# Custom config
# ---------------------------------------------------------
try:
    from sachima_config import *  # noqa
    import sachima_config

    print("Loading local config file: [{}]".format(sachima_config.__file__))
except ImportError as error:
    print("[There is no sachima_config.py. You're not in sachima project.]")


try:
    from cache_list import CACHE_LIST  # noqa
    import cache_list

    print("Loading cache_list file: [{}]".format(cache_list.__file__))
except ImportError as error:
    print("[There is no cache_list.py.]")

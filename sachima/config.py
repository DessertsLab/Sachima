import os


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
# Custom config
# ---------------------------------------------------------
try:
    from sachima_config import *  # noqa
    import sachima_config

    print("Loading local config file: [{}]".format(sachima_config.__file__))
except ImportError:
    pass

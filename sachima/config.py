import os


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# ---------------------------------------------------------
# Superset API
# ---------------------------------------------------------
SUPERSET_WEBSERVER_ADDRESS = 'http://0.0.0.0/'
SUPERSET_WEBSERVER_PORT = 8088
SUPERSET_USERNAME = 'admin'
SUPERSET_PASSWORD = 'general'
SUPERSET_API_TABLE_BP = '/sachima/v1/save_or_overwrite_slice/'

# ---------------------------------------------------------
# 自定义配置
# ---------------------------------------------------------
try:
    from sachima_config import *  # noqa
    import sachima_config
    print('载入本地自定义配置文件： [{}]'.format(
        sachima_config.__file__))
except ImportError:
    pass

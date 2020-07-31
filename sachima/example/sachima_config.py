import logging

# ----------------------------
# amqp broker for rpc api
# ----------------------------
# BROKER = {"AMQP_URI": "amqp://admin:bMT41}ngvy@10.9.134.64:5672"}  # test


# ---------------------------------------------------------
# mail config
# ---------------------------------------------------------
# MAIL_HOST = ""
# MAIL_ADD = ""
# MAIL_USER = ""
# MAIL_PASS = ""
# MAIL_SENDER = ""

# ---------------------------------------------------------
# sns config
# ---------------------------------------------------------
# SNS_DINGDING_ERROR_GRP_TOKEN = (
# )
# SNS_DINGDING_INFO_GRP_TOKEN = (
# )
# SNS_DINGDING_SENDING_STR = "[local]Sending reports {}...{}"
# SNS_DINGDING_ERRSENT_STR = "[local]Report {} err, please check{}"


# ---------------------------------------------------------
# database config
# ---------------------------------------------------------
# IMPALA_IP = ""
# IMPALA_PORT = 21050
# IMPALA_DB = "dw"
# IMPALA_TIMEOUT = 200
# IMPALA_AUTH_MECHANISM = "NOSASL"

# MYSQL_H_DB = ""
# MYSQL_H_IP = ""
# MYSQL_H_USER = "root"
# MYSQL_H_PASS = ""
# MYSQL_H_CHARSET = "utf8"
# MYSQL_H_PORT = 3306

# MYSQL_D_DB = ""
# MYSQL_D_IP = ""
# MYSQL_D_USER = ""
# MYSQL_D_PASS = ""
# MYSQL_D_CHARSET = "utf8"
# MYSQL_D_PORT = 3306

# MARIADB_DB = "dw"
# MARIADB_IP = ""
# MARIADB_USER = "visualdata"
# MARIADB_PASS = ""
# MARIADB_CHARSET = "utf8"
# MARIADB_PORT = 3306

# ---------------------------------------------------------
# geo api config
# ---------------------------------------------------------
BAIDU_GEO_TOKEN = ""
QQ_GEO_TOKEN = ""
AMAP_GEO_TOKEN = ""

# ---------------------------------------------------------
# logging config
# ---------------------------------------------------------
LOG_LEVEL = logging.DEBUG
# LOG_LEVEL = logging.INFO
# LOG_LEVEL = logging.ERROR
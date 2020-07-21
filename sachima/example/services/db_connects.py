"""
if you need to connect Oracle  you shoud install cx_Oracle

mac instanclient install
http://www.oracle.com/technetwork/topics/intel-macsoft-096467.html?ssSourceSiteId=otncn

mkdir ~/lib
ln -s ~/instantclient_12_2/libclntsh.dylib ~/lib/
ln -s ~/instantclient_12_2/libclntsh.dylib.12.1 ~/lib/


https://stackoverflow.com/questions/51170169/clean-up-database-connection-with-sqlalchemy-in-pandas
engine = create_engine('...', poolclass=NullPool)
engine.dispose()
"""
# https://github.com/cloudera/impyla
from impala.dbapi import connect as imp_connect
from pymysql import connect as my_connect
from pymysql import cursors as cursors

# from impala.util import as_pandas
from sqlalchemy import create_engine, MetaData, pool
from sqlalchemy import Table, Column, Date, Integer, String, ForeignKey
from sachima import conf

# ENGINE_ORACLE = create_engine(
#         "oracle+cx_oracle://xxx:xxxx@xxxxx:1521/POS",
#         connect_args={'encoding': 'utf8', 'nencoding': 'utf8'})


class db(object):
    @property
    def ENGINE_SUPERSET(self):
        return create_engine("sqlite:///{}".format(conf.get("DB_SUPERSET")), echo=True)

    @property
    def ENGINE_MYSQL_h(self):
        return create_engine(
            "mysql+pymysql://{}:{}@{}/{}".format(
                conf.get("MYSQL_H_USER"),
                conf.get("MYSQL_H_PASS"),
                conf.get("MYSQL_H_IP"),
                conf.get("MYSQL_H_DB"),
            ),
            connect_args={"charset": conf.get("MYSQL_H_CHARSET")},
            poolclass=pool.NullPool,
        )

    @property
    def ENGINE_MYSQL_d(self):
        return create_engine(
            "mysql+pymysql://{}:{}@{}/{}".format(
                conf.get("MYSQL_D_USER"),
                conf.get("MYSQL_D_PASS"),
                conf.get("MYSQL_D_IP"),
                conf.get("MYSQL_D_DB"),
            ),
            connect_args={"charset": conf.get("MYSQL_D_CHARSET")},
            poolclass=pool.NullPool,
        )

    @property
    def ENGINE_IMPALA_DW(self):
        def _impala_conn():
            return imp_connect(
                host=conf.get("IMPALA_IP"),
                port=conf.get("IMPALA_PORT"),
                database=conf.get("IMPALA_DB"),
                timeout=conf.get("IMPALA_TIMEOUT"),
                #      use_ssl=True,
                #      ca_cert='some_pem',
                #      user='cloudera',
                #      password='cloudera',
                auth_mechanism=conf.get("IMPALA_AUTH_MECHANISM"),
                #      kerberos_service_name='hive'
            )

        return create_engine(
            "impala://", creator=_impala_conn, echo=False, poolclass=pool.NullPool,
        )

    @property
    def ENGINE_MARIADB_dw(self):
        return create_engine(
            "mysql+pymysql://{}:{}@{}/{}".format(
                conf.get("MARIADB_USER"),
                conf.get("MARIADB_PASS"),
                conf.get("MARIADB_IP"),
                conf.get("MARIADB_DB"),
            ),
            connect_args={"charset": conf.get("MARIADB_CHARSET")},
            poolclass=pool.NullPool,
        )

    # ---------------------------------
    # conn
    # ---------------------------------

    @property
    def CONN_IMPALA_DW(self):
        return imp_connect(
            host=conf.get("IMPALA_IP"),
            port=conf.get("IMPALA_PORT"),
            database=conf.get("IMPALA_DB"),
            auth_mechanism=conf.get("IMPALA_AUTH_MECHANISM"),
        )

    @property
    def CONN_MYSQL_h(self):
        return my_connect(
            host=conf.get("MYSQL_H_IP"),
            user=conf.get("MYSQL_H_USER"),
            password=conf.get("MYSQL_H_PASS"),
            port=conf.get("MYSQL_H_PORT"),
            database=conf.get("MYSQL_H_DB"),
            charset=conf.get("MYSQL_H_CHARSET"),
            use_unicode=True,
            cursorclass=cursors.SSDictCursor,
        )

    @property
    def CONN_MYSQL_d(self):
        return my_connect(
            host=conf.get("MYSQL_D_IP"),
            user=conf.get("MYSQL_D_USER"),
            password=conf.get("MYSQL_D_PASS"),
            port=conf.get("MYSQL_D_PORT"),
            database=conf.get("MYSQL_D_DB"),
            charset=conf.get("MYSQL_D_CHARSET"),
            cursorclass=cursors.SSDictCursor,
        )

    # ---------------------------------
    # meta
    # ---------------------------------

    @property
    def MetaData_MYSQL_h(self):
        return MetaData(self.ENGINE_MYSQL_h)

    @property
    def MetaData_MYSQL_d(self):
        return MetaData(self.ENGINE_MYSQL_d)

    @property
    def MetaData_IMPALA_DW(self):
        return MetaData(self.ENGINE_IMPALA_DW)

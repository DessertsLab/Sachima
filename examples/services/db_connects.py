'''
if you need to connect Oracle  you shoud install cx_Oracle

mac instanclient install
http://www.oracle.com/technetwork/topics/intel-macsoft-096467.html?ssSourceSiteId=otncn

mkdir ~/lib
ln -s ~/instantclient_12_2/libclntsh.dylib ~/lib/
ln -s ~/instantclient_12_2/libclntsh.dylib.12.1 ~/lib/
'''
# https://github.com/cloudera/impyla
from impala.dbapi import connect as imp_connect
from pymysql import connect as my_connect
from pymysql import cursors as cursors
# from impala.util import as_pandas
from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, Date, Integer, String, ForeignKey
from sachima import conf

# ENGINE_ORACLE = create_engine(
#         "oracle+cx_oracle://xxx:xxxx@xxxxx:1521/POS",
#         connect_args={'encoding': 'utf8', 'nencoding': 'utf8'})


class db(object):
    def __init__(self):
        self.impala_ip = conf.get("IMPALA_IP")
        self.impala_port = conf.get("IMPALA_PORT")
        self.impala_db = conf.get("IMPALA_DB")
        self.impala_timeout = conf.get("IMPALA_TIMEOUT")
        self.impala_auth_mechanism = conf.get("IMPALA_AUTH_MECHANISM")
        self.mysql_h_db = conf.get("MYSQL_H_DB")
        self.mysql_h_ip = conf.get("MYSQL_H_IP")
        self.mysql_h_port = conf.get("MYSQL_H_PORT")
        self.mysql_h_user = conf.get("MYSQL_H_USER")
        self.mysql_h_pass = conf.get("MYSQL_H_PASS")
        self.mysql_h_charset = conf.get("MYSQL_H_CHARSET")
        self.mysql_d_db = conf.get("MYSQL_D_DB")
        self.mysql_d_ip = conf.get("MYSQL_D_IP")
        self.mysql_d_port = conf.get("MYSQL_D_PORT")
        self.mysql_d_user = conf.get("MYSQL_D_USER")
        self.mysql_d_pass = conf.get("MYSQL_D_PASS")
        self.mysql_d_charset = conf.get("MYSQL_D_CHARSET")
        self.mariadb_db = conf.get("MARIADB_DB")
        self.mariadb_ip = conf.get("MARIADB_IP")
        self.mariadb_port = conf.get("MARIADB_PORT")
        self.mariadb_user = conf.get("MARIADB_USER")
        self.mariadb_pass = conf.get("MARIADB_PASS")
        self.mariadb_charset = conf.get("MARIADB_CHARSET")

    @property
    def ENGINE_SUPERSET(self):
        return create_engine('sqlite:///{}'.format(conf.get("DB_SUPERSET")),
                             echo=True)

    @property
    def ENGINE_MYSQL_hawaii(self):
        return create_engine(
            "mysql+pymysql://{}:{}@{}/{}"
            .format(conf.get("MYSQL_H_USER"),
                    self.mysql_h_pass,
                    self.mysql_h_ip,
                    self.mysql_h_db),
            connect_args={'charset': self.mysql_h_charset}
        )

    @property
    def ENGINE_MYSQL_duckchat(self):
        return create_engine(
            "mysql+pymysql://{}:{}@{}/{}"
            .format(self.mysql_d_user,
                    self.mysql_d_pass,
                    self.mysql_d_ip,
                    self.mysql_d_db),
            connect_args={'charset': self.mysql_d_charset}
        )

    @property
    def ENGINE_IMPALA_DW(self):
        _impala_conn = imp_connect(
            host=self.impala_ip,
            port=self.impala_port,
            database=self.impala_db,
            timeout=self.impala_timeout,
            #      use_ssl=True,
            #      ca_cert='some_pem',
            #      user='cloudera',
            #      password='cloudera',
            auth_mechanism=self.impala_auth_mechanism,
            #      kerberos_service_name='hive'
        )
        return create_engine(
            'impala://', creator=_impala_conn, echo=False)

    @property
    def ENGINE_MARIADB_dw(self):
        return create_engine(
            "mysql+pymysql://{}:{}@{}/{}"
            .format(self.mariadb_user,
                    self.mariadb_pass,
                    self.mariadb_ip,
                    self.mariadb_db),
            connect_args={'charset': self.mariadb_charset}
        )

    @property
    def CONN_IMPALA_DW(self):
        return imp_connect(
            host=self.impala_ip,
            port=self.impala_port,
            database=self.impala_db,
            auth_mechanism=self.impala_auth_mechanism)

    @property
    def CONN_MYSQL_hawaii(self):
        return my_connect(
            host=self.mysql_h_ip,
            user=self.mysql_h_user,
            password=self.mysql_h_pass,
            port=self.mysql_h_port,
            database=self.mysql_h_db,
            charset=self.mysql_h_charset,
            cursorclass=cursors.SSDictCursor)

    @property
    def CONN_MYSQL_duckchat(self):
        return my_connect(
            host=self.mysql_d_ip,
            user=self.mysql_d_user,
            password=self.mysql_d_pass,
            port=self.mysql_d_port,
            database=self.mysql_d_db,
            charset=self.mysql_d_charset,
            cursorclass=cursors.SSDictCursor)

    @property
    def MetaData_MYSQL_hawaii(self):
        return MetaData(self.ENGINE_MYSQL_hawaii)

    @property
    def MetaData_MYSQL_duckchat(self):
        return MetaData(self.ENGINE_MYSQL_duckchat)

    @property
    def MetaData_IMPALA_DW(self):
        return MetaData(self.ENGINE_IMPALA_DW)

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
import yaml

# ENGINE_ORACLE = create_engine(
#         "oracle+cx_oracle://xxx:xxxx@xxxxx:1521/POS",
#         connect_args={'encoding': 'utf8', 'nencoding': 'utf8'})


class db(object):
    def __init__(self):
        with open('conf/sachima.yaml', 'r') as f:
            c = yaml.load(f)
            self.impala_ip = c['db']['impala']['ip']
            self.impala_port = c['db']['impala']['port']
            self.impala_db = c['db']['impala']['db']
            self.impala_timeout = c['db']['impala']['timeout']
            self.impala_auth_mechanism = c['db']['impala']
            ['impala_auth_mechanism']
            self.mysql_h_db = c['db']['mysql_h']['db']
            self.mysql_h_ip = c['db']['mysql_h']['ip']
            self.mysql_h_port = c['db']['mysql_h']['port']
            self.mysql_h_user = c['db']['mysql_h']['user']
            self.mysql_h_pass = c['db']['mysql_h']['pass']
            self.mysql_h_charset = c['db']['mysql_h']['charset']
            self.mysql_d_db = c['db']['mysql_d']['db']
            self.mysql_d_ip = c['db']['mysql_d']['ip']
            self.mysql_d_port = c['db']['mysql_d']['port']
            self.mysql_d_user = c['db']['mysql_d']['user']
            self.mysql_d_pass = c['db']['mysql_d']['pass']
            self.mysql_d_charset = c['db']['mysql_d']['charset']
            self.mariadb_db = c['db']['mariadb']['db']
            self.mariadb_ip = c['db']['mariadb']['ip']
            self.mariadb_port = c['db']['mariadb']['port']
            self.mariadb_user = c['db']['mariadb']['user']
            self.mariadb_pass = c['db']['mariadb']['pass']
            self.mariadb_charset = c['db']['mariadb']['charset']
        print('Loading database config from conf/sachima.yaml')

    @property
    def ENGINE_MYSQL_hawaii(self):
        return create_engine(
            "mysql+pymysql://{}:{}@{}/{}"
            .format(self.mysql_h_user,
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

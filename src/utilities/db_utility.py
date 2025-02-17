import pymysql
import os
import logging as logger
import dotenv
import allure

from src.utilities.credentials_utility import CredentialsUtility
from src.configs.hosts_config import DB_HOST


dotenv.load_dotenv()


class DBUtility(object):

    def __init__(self):
        creds_helper = CredentialsUtility()
        self.creds = creds_helper.get_db_credentials()

        self.machine = os.environ.get('MACHINE')
        assert self.machine, f"Environment variable 'MACHINE' must be set."

        self.wp_host = os.environ.get('WP_HOST')
        assert self.wp_host, f"Environment variable 'WP_HOST' must be set."

        if self.machine == 'docker' and self.wp_host == 'local':
            raise Exception(f"Can not run test in docker if WP_HOST=local")

        self.env = os.environ.get('ENV', 'test')
        self.host = DB_HOST[self.machine][self.env]['host']
        self.socket = DB_HOST[self.machine][self.env]['socket']
        self.port = DB_HOST[self.machine][self.env]['port']
        self.database = DB_HOST[self.machine][self.env]['database']
        self.table_prefix = DB_HOST[self.machine][self.env]['table_prefix']

    def create_connection(self):
        """Create connection to DB"""

        if self.wp_host == 'ampps':
            connection = pymysql.connect(host=self.host, user=self.creds['db_user'],
                                         password=self.creds['db_password'],
                                         unix_socket=self.socket)
        elif self.wp_host == 'local':
            connection = pymysql.connect(host=self.host, user=self.creds['db_user'],
                                         password=self.creds['db_password'],
                                         port=self.port)
        else:
            raise Exception("Unknown WP_HOST.")
        return connection

    def execute_select(self, sql):
        """Execute SQL SELECT"""

        with allure.step(f"Create connection to DB"):
            conn = self.create_connection()
        with allure.step(f"Execute SQL SELECT"):
            try:
                # logger.debug(f"Executing: {sql}")
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                cursor.execute(sql)
                result_select = cursor.fetchall()
                cursor.close()
            except Exception as e:
                raise Exception(f"Failed running sql: {sql} \n  Error: {str(e)}")
            finally:
                conn.close()
            return result_select

    def execute_sql(self, sql):
        pass

import random

from src.utilities.db_utility import DBUtility


class CustomersDAO(object):
    """
    The 'Customer' class allows you to select of customer from DB
    """

    def __init__(self):
        self.db_helper = DBUtility()

    def get_customer_by_email(self, email) -> list:
        """
        Get customer by email from DB
        """

        sql = f"""SELECT * FROM {self.db_helper.database}.{self.db_helper.table_prefix}users 
                  WHERE user_email='{email}';"""
        result_select = self.db_helper.execute_select(sql)
        return result_select

    def get_random_customer_from_db(self, qty=1) -> list:
        """
        Get random customer from DB
        """

        sql = f"""SELECT * FROM {self.db_helper.database}.{self.db_helper.table_prefix}users 
                  ORDER BY id DESC LIMIT 5000;"""
        result_select = self.db_helper.execute_select(sql)
        return random.sample(result_select, int(qty))

import random

from src.utilities.db_utility import DBUtility


class ProductsDAO(object):

    def __init__(self):
        self.db_helper = DBUtility()

    def get_random_products(self, quantity=1):
        sql = f"""SELECT * FROM {self.db_helper.database}.{self.db_helper.table_prefix}posts 
                  WHERE post_type='product' LIMIT 500;"""
        response_sql_all = self.db_helper.execute_select(sql)
        response_sql = random.sample(response_sql_all, int(quantity))
        return response_sql

    def get_product_by_id(self, product_id) -> list:
        """Get product from DB by 'id'"""

        sql = f"""SELECT * FROM {self.db_helper.database}.{self.db_helper.table_prefix}posts 
                  WHERE ID={product_id};"""
        result_select = self.db_helper.execute_select(sql)
        return result_select

    def get_products_created_after_given_date(self, created_date):
        sql = f"""SELECT * FROM {self.db_helper.database}.{self.db_helper.table_prefix}posts 
                  WHERE post_type='product' AND post_date>'{created_date}' 
                  LIMIT 10000;"""
        response_sql = self.db_helper.execute_select(sql)
        return response_sql

    def get_random_products_that_are_not_on_sale(self, quantity=1):
        sql = f"""SELECT * FROM {self.db_helper.database}.{self.db_helper.table_prefix}posts WHERE post_type='product' AND id NOT IN 
                    (SELECT post_id FROM {self.db_helper.database}.{self.db_helper.table_prefix}postmeta WHERE meta_key='_sale_price');"""
        response_sql_all = self.db_helper.execute_select(sql)
        response_sql = random.sample(response_sql_all, int(quantity))
        return response_sql

    def get_random_products_that_are_on_sale(self, quantity=1):
        sql = f"""SELECT * FROM {self.db_helper.database}.{self.db_helper.table_prefix}posts WHERE post_type = 'product' AND id IN 
                    (SELECT post_id FROM {self.db_helper.database}.{self.db_helper.table_prefix}postmeta WHERE `meta_key`="_sale_price");"""
        response_sql_all = self.db_helper.execute_select(sql)
        response_sql = random.sample(response_sql_all, int(quantity))
        return response_sql

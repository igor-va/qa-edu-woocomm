import os
import json

from src.utilities.woo_api_utility import WooAPIUtility
from src.dao.orders_dao import OrdersDAO
from src.endpoints.endpoints import Endpoints


class OrdersHelper(object):

    def __init__(self):
        self.current_file_dir = os.path.dirname(os.path.realpath(__file__))
        self.woo_helper = WooAPIUtility()

    def create_order(self, payload_additional=None):
        payload_template = os.path.join(self.current_file_dir, '..', 'data', 'create_order_payload.json')

        # In the data (create_order_payload.json) verify the product id used exists, "line_items": {"product_id": 12,"quantity": 1}
        # If the product does not exist you will get 'completed' as the default status of the order when created.
        # The default should be 'processing' if the product is valid.
        with open(payload_template) as f:
            payload = json.load(f)

        # If user adds more info to payload, then update it
        if payload_additional:
            assert isinstance(payload_additional, dict), \
                f"Parameter 'additional_args' must be a 'dictionary', but found '{type(payload_additional)}'."
            payload.update(payload_additional)

        response_json = self.woo_helper.post(Endpoints.orders, params=payload, expected_status_code=201)

        return response_json

    @staticmethod
    def verify_order_is_created(order_response_json, customer_expected_id, products_expected):
        orders_dao = OrdersDAO()

        # Verify response
        assert order_response_json, f"Create order response is empty."
        assert order_response_json['customer_id'] == customer_expected_id, \
            f"Create order with given 'customer_id' returned bad 'customer_id', \
            expected '{customer_expected_id}', but got '{order_response_json['customer_id']}'."
        assert len(order_response_json['line_items']) == len(products_expected), \
            f"Expected '{len(products_expected)}' item in order, but found '{len(order_response_json['line_items'])}'."

        # Verify db
        order_response_id = order_response_json['id']
        order_database = orders_dao.get_order_lines_by_order_id(order_response_id)
        assert order_database, f"Create order, line item not found in DB. Order id: {order_response_id}"

        line_items = [i for i in order_database if i['order_item_type'] == 'line_item']
        assert len(line_items) == 1, \
            f"Expected 1 line item, but found '{len(line_items)}', order id '{order_response_id}'."

        # get list of product ids in the response
        api_product_ids = [i['product_id'] for i in order_response_json['line_items']]

        for product in products_expected:
            assert product['product_id'] in api_product_ids, \
                f"Create order does not have at least 1 expected product in DB, \
                product id '{product['product_id']}', order id '{order_response_id}'."

    def call_update_an_order(self, order_id, payload, exp_st_code=200):
        response_json = self.woo_helper.put(f'{Endpoints.orders}/{order_id}', params=payload, expected_status_code=exp_st_code)
        return response_json

    def call_retrieve_an_order(self, order_id):
        response_json = self.woo_helper.get(f"{Endpoints.orders}/{order_id}")
        return response_json

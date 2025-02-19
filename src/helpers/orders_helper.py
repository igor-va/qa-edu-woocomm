import os
import json
import allure

from src.utilities.requests_utility import RequestsUtility
from src.dao.orders_dao import OrdersDAO
from src.endpoints.endpoints import Endpoints


class OrdersHelper(object):
    """
    The orders API allows you to create, view, update, and delete individual, or a batch, of orders.
    """

    def __init__(self):
        self.current_file_dir = os.path.dirname(os.path.realpath(__file__))
        self.requests_utility = RequestsUtility()

    def call_create_order(self, payload_add=None) -> dict:
        """
        Call 'Create an order', this API helps you to create a new order.
        In the data (create_order_payload.json) verify the product id used exists, "line_items": {"product_id": 12,"quantity": 1}
        If the product does not exist you will get 'completed' as the default status of the order when created.
        The default should be 'processing' if the product is valid.
        """

        # Load data from json payload template
        payload_template_file = os.path.join(self.current_file_dir, '..', 'data', 'create_order_payload.json')
        with open(payload_template_file) as f:
            payload_all = json.load(f)
        # If user adds more info to payload, then update it
        if payload_add:
            assert isinstance(payload_add, dict), \
                f"Parameter 'payload_add' must be a 'dictionary', but found {type(payload_add)}."
            payload_all.update(payload_add)
        response_json = self.requests_utility.post(Endpoints.orders, payload=payload_all, expected_status_code=201)
        return response_json

    @staticmethod
    def verify_order_is_created(order_api, customer_id_expected, products_id_expected, payload) -> None:
        """
        Verify order is created
        """

        with allure.step(f"Verify API"):
            assert order_api, f"Create order response is empty."
            assert order_api['customer_id'] == customer_id_expected, \
                f"Return wrong 'customer_id', expected {customer_id_expected}, actual {order_api['customer_id']}."
            assert len(order_api['line_items']) == len(products_id_expected), \
                f"Item in order expected {len(products_id_expected)}, actual {len(order_api['line_items'])}."
        with allure.step(f"Verify DB"):
            orders_dao = OrdersDAO()
            order_api_id = order_api['id']
            order_db = orders_dao.get_order_lines_by_order_id(order_api_id)
            assert order_db, \
                f"Order 'id' {order_api_id} not found in DB."
            line_items = [i for i in order_db if i['order_item_type'] == 'line_item']
            assert len(line_items) == len(payload['line_items']), \
                f"Expected 'line_items' {len(payload['line_items'])}, actual {len(line_items)}, order id {order_api_id}."
        with allure.step(f"Verify product 'ID' in the API have in DB"):
            api_products_id = [i['product_id'] for i in order_api['line_items']]
            for product in products_id_expected:
                assert product['product_id'] in api_products_id, \
                    f"Product 'id' {product['product_id']} not have in DB, order 'id' {order_api_id}."

    def call_update_an_order(self, order_id, payload, exp_st_code=200) -> dict:
        """
        Call 'Update an Order', this API lets you make changes to an order.
        """

        response_json = self.requests_utility.put(f'{Endpoints.orders}/{order_id}', payload=payload, expected_status_code=exp_st_code)
        return response_json

    def call_retrieve_an_order(self, order_id) -> dict:
        """
        Call 'Retrieve an order', this API lets you retrieve and view a specific order.
        """

        response_json = self.requests_utility.get(f"{Endpoints.orders}/{order_id}")
        return response_json

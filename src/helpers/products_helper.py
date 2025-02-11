import logging as logger

from src.utilities.requests_utility import RequestsUtility
from src.endpoints.endpoints import Endpoints


class ProductsHelper(object):

    def __init__(self):
        self.requests_utility = RequestsUtility()

    def get_product_by_id(self, product_id):
        response_json = self.requests_utility.get(f"{Endpoints.products}/{product_id}")
        return response_json

    def call_create_product(self, payload) -> dict:
        """Call create product"""

        response_json = self.requests_utility.post(Endpoints.products, payload=payload, expected_status_code=201)
        return response_json

    def call_list_products(self, payload=None):
        max_pages = 1000
        response_json = []
        for i in range(1, max_pages + 1):
            logger.debug(f"List products page number: {i}")

            if not payload:
                payload = {}

            if 'per_page' not in payload.keys():
                payload['per_page'] = 100

            # Add the current page number to the call
            payload['page'] = i
            response_json_part = self.requests_utility.get(Endpoints.products, payload=payload)

            # If there not is response then stop the loop b/c there are no more products
            if not response_json_part:
                break
            else:
                response_json.extend(response_json_part)
        else:
            raise Exception(f"Unable to find all products after {max_pages} pages.")

        return response_json

    def call_retrieve_product_by_id(self, product_id):
        response_json = self.requests_utility.get(f"{Endpoints.products}/{product_id}")
        return response_json

    def call_update_product(self, product_id, payload=None):
        response_json = self.requests_utility.put(f"{Endpoints.products}/{product_id}", payload=payload)
        return response_json

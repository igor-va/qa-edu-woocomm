import logging as logger

from src.utilities.requests_utility import RequestsUtility
from src.endpoints.endpoints import Endpoints


class ProductsHelper(object):

    def __init__(self):
        self.requests_utility = RequestsUtility()

    def get_product_by_id(self, product_id):
        return self.requests_utility.get(f"{Endpoints.products}/{product_id}")

    def call_create_product(self, payload):
        return self.requests_utility.post(Endpoints.products, payload=payload, expected_status_code=201)

    def call_list_products(self, payload=None):
        max_pages = 1000
        products_response = []
        for i in range(1, max_pages + 1):
            logger.debug(f"List products page number: {i}")

            if not payload:
                payload = {}

            if 'per_page' not in payload.keys():
                payload['per_page'] = 100

            # add the current page number to the call
            payload['page'] = i
            response_json = self.requests_utility.get(Endpoints.products, payload=payload)

            # If there not is response then stop the loop b/c there are no more products
            if not response_json:
                break
            else:
                products_response.extend(response_json)
        else:
            raise Exception(f"Unable to find all products after {max_pages} pages.")

        return products_response

    def call_retrieve_product(self, product_id):
        return self.requests_utility.get(f'products/{product_id}')

    def call_update_product(self, product_id, payload=None):
        return self.requests_utility.put(f'products/{product_id}', payload=payload)

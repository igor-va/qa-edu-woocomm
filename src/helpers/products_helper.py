import logging as logger

from src.utilities.requests_utility import RequestsUtility
from src.endpoints.endpoints import Endpoints


class ProductsHelper(object):
    """
    The 'Products' API class allows you to create, view, update, and delete individual or a batch of products
    """

    def __init__(self):
        self.requests_utility = RequestsUtility()

    def call_create_product(self, payload) -> dict:
        """
        Call 'Create a product'
        """

        response_json = self.requests_utility.post(Endpoints.products, payload=payload, expected_status_code=201)
        return response_json

    def call_retrieve_product_by_id(self, product_id) -> dict:
        """
        Call 'Retrieve a product'
        """

        response_json = self.requests_utility.get(f"{Endpoints.products}/{product_id}")
        return response_json

    def call_list_all_products(self) -> list:
        """
        Call 'List all products'
        """

        response_json = self.requests_utility.get(Endpoints.products)
        return response_json

    def call_list_products_with_filter(self, payload=None) -> list:
        """
        Call 'List all products' with filter
        """

        max_pages = 1000
        response_json = []
        for i in range(1, max_pages + 1):
            logger.debug(f"List products page number: {i}")
            if not payload:  # Add payload data if None
                payload = {}
            if 'per_page' not in payload.keys():  # Add number of items to be returned in result set
                payload['per_page'] = 100
            payload['page'] = i  # Add the current page number to the call

            # Sends a GET request
            response_json_part = self.requests_utility.get(Endpoints.products, payload=payload)

            # If there not is response then stop the loop b/c there are no more products
            if not response_json_part:
                break
            else:
                response_json.extend(response_json_part)
        else:
            raise Exception(f"Unable to find all products after {max_pages} pages.")
        return response_json

    def call_update_product(self, product_id, payload=None) -> dict:
        """
        Call 'Update a product'
        """

        response_json = self.requests_utility.put(f"{Endpoints.products}/{product_id}", payload=payload)
        return response_json

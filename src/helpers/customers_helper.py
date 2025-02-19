from src.utilities.generic_utilities import *
from src.utilities.requests_utility import RequestsUtility
from src.endpoints.endpoints import Endpoints


class CustomersHelper(object):
    """
    The customer API allows you to create, view, update, and delete individual, or a batch, of customers.
    """

    def __init__(self):
        self.requests_utility = RequestsUtility()

    def create_customer(self, email=None, password=None, exp_st_code=201, **kwargs) -> dict:
        """
        This API helps you to create a new customer.
        """

        if not email:
            email = generate_random_email()
        if not password:
            password = generate_random_password()
        payload = dict()
        payload['email'] = email
        payload['password'] = password
        payload.update(kwargs)

        response_json = self.requests_utility.post(Endpoints.customers, payload=payload, expected_status_code=exp_st_code)
        return response_json

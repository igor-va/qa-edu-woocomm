from src.utilities.generic_utilities import generate_random_email_and_password
from src.utilities.requests_utility import RequestsUtility
from src.endpoints.endpoints import Endpoints


class CustomerHelper(object):

    def __init__(self):
        self.requests_utility = RequestsUtility()

    def create_customer(self, email=None, password=None, exp_st_code=201, **kwargs) -> dict:

        if not email:
            ep = generate_random_email_and_password()
            email = ep['email']
        if not password:
            password = 'Password1'

        payload = dict()
        payload['email'] = email
        payload['password'] = password
        payload.update(kwargs)

        response_json = self.requests_utility.post(Endpoints.customers, payload=payload, expected_status_code=exp_st_code)

        return response_json

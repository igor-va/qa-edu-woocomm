from src.utilities.genericUtilities import generate_random_email_and_password
from src.utilities.requestsUtility import RequestsUtility
from src.endpoints.endpoints import Endpoints


class CustomerHelper(object):

    def __init__(self):
        self.requests_utility = RequestsUtility()

    def create_customer(self, email=None, password=None, **kwargs) -> dict:

        if not email or not password:
            ep = generate_random_email_and_password()
            email = ep['email']
            password = ep['password']

        payload = dict()
        payload['email'] = email
        payload['password'] = password
        payload.update(kwargs)

        response_json = self.requests_utility.post(Endpoints.customers, payload=payload, expected_status_code=201)

        return response_json

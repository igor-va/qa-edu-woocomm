import os
import logging as logger
import pdb

from src.configs.hosts_config import WOO_API_HOSTS
from src.utilities.credentials_utility import CredentialsUtility
from woocommerce import API


class WooAPIUtility(object):

    def __init__(self):
        wc_creds = CredentialsUtility.get_wc_api_keys()
        self.env = os.environ.get('ENV', 'test')
        self.base_url = WOO_API_HOSTS[self.env]
        self.wcapi = API(
            url=self.base_url,
            consumer_key=wc_creds['wc_key'],
            consumer_secret=wc_creds['wc_secret'],
            version="wc/v3"
        )

    @staticmethod
    def assert_status_code(status_code, expected_status_code):
        assert status_code == expected_status_code, \
            f"Bad 'Status code', expected '{expected_status_code}', actual returned: '{status_code}'."

    def post(self, wc_endpoint, params=None, expected_status_code=200):
        response_api = self.wcapi.post(wc_endpoint, data=params)
        status_code = response_api.status_code
        response_json = response_api.json()
        self.assert_status_code(status_code, expected_status_code)
        logger.debug(f"POST API response: {response_json}")
        return response_json

    def get(self, wc_endpoint, params=None, expected_status_code=200):
        response_api = self.wcapi.get(wc_endpoint, params=params)
        status_code = response_api.status_code
        response_json = response_api.json()
        self.assert_status_code(status_code, expected_status_code)
        logger.debug(f"GET API response: {response_json}")
        return response_json

    def put(self, wc_endpoint, params=None, expected_status_code=200):
        response_api = self.wcapi.put(wc_endpoint, data=params)
        status_code = response_api.status_code
        response_json = response_api.json()
        self.assert_status_code(status_code, expected_status_code)
        logger.debug(f"PUT API response: {response_json}")
        return response_json


if __name__ == '__main__':

    obj = WooAPIUtility()
    rs_api = obj.get('products')
    print(rs_api)
    pdb.set_trace()

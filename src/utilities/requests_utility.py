import requests
import os
from requests_oauthlib import OAuth1
import logging as logger
import allure

from src.configs.hosts_config import API_HOSTS
from src.utilities.credentials_utility import CredentialsUtility


class RequestsUtility(object):
    """
    Requests API Utility
    """

    def __init__(self):
        wc_creds = CredentialsUtility.get_wc_api_keys()
        self.env = os.environ.get('ENV', 'test')
        self.base_url = API_HOSTS[self.env]
        self.auth = OAuth1(wc_creds['wc_key'], wc_creds['wc_secret'])
        self.requests = requests

    @staticmethod
    def assert_status_code(status_code, expected_status_code) -> None:
        assert status_code == expected_status_code, \
            f"Bad 'status_code', expected {expected_status_code}, actual {status_code}."

    def post(self, endpoint, payload=None, headers=None, expected_status_code=200) -> dict:
        """
        Sends a POST request
        """

        with allure.step(f"Make the 'POST request'"):
            url = self.base_url + endpoint
            response_api = self.requests.post(url=url, json=payload, headers=headers, auth=self.auth)
        with allure.step(f"Verify 'status code'"):
            status_code = response_api.status_code
            self.assert_status_code(status_code, expected_status_code)
        with allure.step(f"Returned 'response'"):
            response_json = response_api.json()
            return response_json

    def get(self, endpoint, payload=None, headers=None, expected_status_code=200) -> dict | list:
        """
        Sends a GET request
        """

        with allure.step(f"Make the 'GET request'"):
            url = self.base_url + endpoint
            response_api = requests.get(url=url, json=payload, headers=headers, auth=self.auth)
        with allure.step(f"Verify 'status code'"):
            status_code = response_api.status_code
            self.assert_status_code(status_code, expected_status_code)
        with allure.step(f"Returned 'response'"):
            response_json = response_api.json()
            return response_json

    def put(self, endpoint, payload=None, headers=None, expected_status_code=200) -> dict:
        """
        Sends a PUT request
        """

        with allure.step(f"Make the 'PUT request'"):
            url = self.base_url + endpoint
            response_api = requests.put(url=url, json=payload, headers=headers, auth=self.auth)
        with allure.step(f"Verify 'status code'"):
            status_code = response_api.status_code
            self.assert_status_code(status_code, expected_status_code)
        with allure.step(f"Returned 'response'"):
            response_json = response_api.json()
            return response_json

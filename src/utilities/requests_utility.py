import requests
import os
import json
from requests_oauthlib import OAuth1
import logging as logger

from src.configs.hosts_config import API_HOSTS
from src.utilities.credentials_utility import CredentialsUtility


class RequestsUtility(object):

    def __init__(self):
        wc_creds = CredentialsUtility.get_wc_api_keys()
        self.env = os.environ.get('ENV', 'test')
        self.base_url = API_HOSTS[self.env]
        self.auth = OAuth1(wc_creds['wc_key'], wc_creds['wc_secret'])

    @staticmethod
    def assert_status_code(url, status_code, expected_status_code, response_json):
        assert status_code == expected_status_code, \
            f"Bad 'Status code', expected '{expected_status_code}', actual returned: '{status_code}'," \
            f"URL: {url}, Response Json: {response_json}"

    def post(self, endpoint, payload=None, headers=None, expected_status_code=200):
        url = self.base_url + endpoint
        response_api = requests.post(url=url, json=payload, headers=headers, auth=self.auth)
        status_code = response_api.status_code
        response_json = response_api.json()
        self.assert_status_code(url, status_code, expected_status_code, response_json)
        logger.debug(f"POST API response: {response_json}")
        return response_json

    def get(self, endpoint, payload=None, headers=None, expected_status_code=200):
        url = self.base_url + endpoint
        response_api = requests.get(url=url, json=payload, headers=headers, auth=self.auth)
        status_code = response_api.status_code
        response_json = response_api.json()
        self.assert_status_code(url, status_code, expected_status_code, response_json)
        logger.debug(f"GET API response: {response_json}")
        return response_json

    def put(self, endpoint, payload=None, headers=None, expected_status_code=200):
        url = self.base_url + endpoint
        response_api = requests.put(url=url, json=payload, headers=headers, auth=self.auth)
        status_code = response_api.status_code
        response_json = response_api.json()
        self.assert_status_code(url, status_code, expected_status_code, response_json)
        logger.debug(f"PUT API response: {response_json}")
        return response_json

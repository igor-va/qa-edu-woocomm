import logging as logger

from src.utilities.requests_utility import RequestsUtility
from src.endpoints.endpoints import Endpoints


class CouponsHelper(object):

    def __init__(self):
        self.requests_utility = RequestsUtility()

    def call_create_coupon(self, payload, exp_st_code=201):
        logger.debug("Calling 'Create Coupon'.")
        response_json = self.requests_utility.post(Endpoints.coupons, payload=payload, expected_status_code=201)
        return response_json

    def call_retrieve_coupon(self, coupon_id):
        logger.debug("Calling retrieve a coupon. Coupon id: {}")
        response_json = self.requests_utility.get(f'{Endpoints.coupons}/{coupon_id}')
        return response_json

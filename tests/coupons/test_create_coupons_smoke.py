import pytest
import logging as logger

from src.utilities.generic_utilities import *


pytestmark = [pytest.mark.coupons, pytest.mark.regression]


@pytest.mark.parametrize("discount_type", [
                             pytest.param(None, marks=[pytest.mark.tcid36, pytest.mark.smoke]),
                             pytest.param('percent', marks=[pytest.mark.tcid37, pytest.mark.smoke]),
                             pytest.param('fixed_product', marks=pytest.mark.tcid38),
                             pytest.param('fixed_cart', marks=pytest.mark.tcid39),
                         ])
def test_create_coupon_percent_discount_type(my_setup, discount_type):
    """
    Creates a coupon with given 'discount_type' verify the coupon is created.
    """

    logger.info("Testing create coupon api for 50% off coupon.")

    # One of the tests is for not sending discount type and verify the default is used, is if None is given check for default
    expected_discount_type = discount_type if discount_type else 'fixed_cart'

    # Get the helper object
    coupons_helper = my_setup['coupons_helper']

    # Prepare data and call api
    amount_percent = generate_random_number_float(min_value=50, max_value=90)
    coupon_code = generate_random_coupon_code()
    payload = dict()
    payload['code'] = coupon_code
    payload['amount'] = amount_percent
    if discount_type:
        payload['discount_type'] = discount_type
    coupon_response = coupons_helper.call_create_coupon(payload=payload)

    # Call API coupon
    coupon_response_id = coupon_response['id']
    coupon_response_check = coupons_helper.call_retrieve_coupon(coupon_response_id)

    # Verify the response
    assert coupon_response_check['amount'] == amount_percent, \
        f"Expected '{amount_percent}', actual '{coupon_response_check['amount']}'."
    assert coupon_response_check['code'] == coupon_code.lower(), \
        f"Expected '{coupon_code.lower()}', actual '{coupon_response_check['code']}'."
    assert coupon_response_check['discount_type'] == expected_discount_type, \
        f"Expected '{expected_discount_type}', actual '{coupon_response_check['discount_type']}'."


@pytest.mark.tcid40
def test_create_coupon_with_invalid_discount_type(my_setup):
    """
    Verifies using a random string in 'discount_type' of create order will fail with correct error message.
    """

    logger.info("Testing create coupon api for with invalid 'discount_type'.")

    # Get the helper object
    coupons_helper = my_setup['coupons_helper']

    # Prepare data and call api
    payload = dict()
    payload['code'] = generate_random_coupon_code()
    payload['amount'] = generate_random_number_float(min_value=50, max_value=90)
    payload['discount_type'] = generate_random_string()
    coupon_response = coupons_helper.call_create_coupon(payload=payload, exp_st_code=400)

    assert coupon_response['code'] == 'rest_invalid_param', \
        f"Crete coupon with invalid 'discount_type', returned code '{coupon_response['code']}', \
        but expected code = 'rest_invalid_param'."
    assert coupon_response['message'] == 'Invalid parameter(s): discount_type', \
        f"Crete coupon with invalid 'discount_type' returned 'message' = '{coupon_response['message']}', \
        but expected message = 'Invalid parameter(s): discount_type'."

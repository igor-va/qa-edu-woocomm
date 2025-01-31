import pytest

from src.helpers.orders_helper import OrdersHelper
from src.utilities.woo_api_utility import WooAPIUtility
from src.utilities.generic_utilities import *


pytestmark = [pytest.mark.orders, pytest.mark.regression]


@pytest.mark.parametrize("new_status",
                         [
                             pytest.param('cancelled', marks=[pytest.mark.tcid55, pytest.mark.smoke]),
                             pytest.param('processing', marks=pytest.mark.tcid56),
                             pytest.param('on-hold', marks=pytest.mark.tcid57),
                         ])
def test_update_order_status(new_status):
    # Create new order
    orders_helper = OrdersHelper()
    order_response_cur = orders_helper.create_order()
    current_status = order_response_cur['status']
    assert current_status != new_status, \
        f"Current status of order is already '{new_status}',unable to run test."

    # Update the status
    order_id = order_response_cur['id']
    payload = {"status": new_status}
    orders_helper.call_update_an_order(order_id, payload)

    # Get order information
    order_response_new = orders_helper.call_retrieve_an_order(order_id)

    # Verify the new order status is what was updated
    assert order_response_new['status'] == new_status, \
        f"Updated order status to '{new_status}', but order is still '{order_response_new['status']}'."


@pytest.mark.tcid58
def test_update_order_status_to_random_string():
    # Generate random 'status'
    new_status = generate_random_string().lower()

    # Create new order
    orders_helper = OrdersHelper()
    order_response_cur = orders_helper.create_order()
    order_id = order_response_cur['id']

    # Update the 'status'
    payload = {"status": new_status}
    order_response_new = orders_helper.call_update_an_order(order_id, payload, exp_st_code=400)

    # Verify 'status' is not update in database
    assert order_response_new['code'] == 'rest_invalid_param', \
        f"Update order status to random string did not have correct code in response, \
        expected 'rest_invalid_param', but actual '{order_response_new['code']}'."
    assert order_response_new['message'] == 'Invalid parameter(s): status',  \
        f"Update order status to random string did not have correct message in response, \
        expected 'rest_invalid_param', but actual: '{order_response_new['message']}'."


@pytest.mark.tcid59
def test_update_order_customer_note():
    # Create new order
    orders_helper = OrdersHelper()
    order_response_cur = orders_helper.create_order()
    order_id = order_response_cur['id']

    # Update the 'customer_note'
    customer_note = generate_random_sentence()
    payload = {"customer_note": customer_note}
    orders_helper.call_update_an_order(order_id, payload)

    # Get order information
    order_response_new = orders_helper.call_retrieve_an_order(order_id)

    # Verify the 'customer_note' is what was updated
    assert order_response_new['customer_note'] == customer_note, \
        f"Update order's 'customer_note' field failed, \
        expected '{customer_note}', but actual '{order_response_new['customer_note']}'."

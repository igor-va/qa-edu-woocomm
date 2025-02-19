import pytest
import allure

from src.helpers.orders_helper import OrdersHelper
from src.utilities.generic_utilities import *


pytestmark = [pytest.mark.orders, pytest.mark.regression]


@allure.feature("Orders")
@allure.story("Create an order")
class TestUpdateOrder(object):
    """
    Tests for 'Update an Order'
    """

    @pytest.mark.parametrize("status_new",
                             [
                                 pytest.param('cancelled', marks=[pytest.mark.smoke]),
                                 pytest.param('completed'),
                                 pytest.param('on-hold'),
                             ])
    @allure.title("TCID-55 Test update order status")
    @allure.description("Update order status to 'canceled', to 'completed’, to 'on-hold'")
    @pytest.mark.tcid55
    def test_update_order_status(self, status_new) -> None:
        """
        Update order status to 'canceled', to 'completed', to 'on-hold'
        """

        with allure.step(f"Make the call 'Create an order'"):
            orders_helper = OrdersHelper()
            order_api = orders_helper.call_create_order()
            status_current = order_api['status']
        with allure.step(f"Verify 'status' in response"):
            assert status_current != status_new, \
                f"Current status of order is already {status_new},unable to run test."
        with allure.step(f"Update the status"):
            order_api_id = order_api['id']
            payload = {"status": status_new}
            orders_helper.call_update_an_order(order_api_id, payload)
        with allure.step(f"Get order information"):
            order_api = orders_helper.call_retrieve_an_order(order_api_id)
        with allure.step(f"Verify the new order status is what was updated"):
            assert order_api['status'] == status_new, \
                f"Updated order status to {status_new}, but order is still {order_api['status']}."

    @pytest.mark.tcid58
    def test_update_order_status_to_random_string(self):
        # Generate random 'status'
        new_status = generate_random_string().lower()

        # Create new order
        orders_helper = OrdersHelper()
        order_response_cur = orders_helper.call_create_order()
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
    def test_update_order_customer_note(self):
        # Create new order
        orders_helper = OrdersHelper()
        order_response_cur = orders_helper.call_create_order()
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

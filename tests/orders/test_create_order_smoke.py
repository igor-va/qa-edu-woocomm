import pytest
import allure

from src.helpers.customers_helper import CustomersHelper
from src.utilities.generic_utilities import *


pytestmark = [pytest.mark.orders, pytest.mark.smoke]


@allure.feature("Orders")
@allure.story("Create an order")
class TestCreateOrder(object):
    """
    Tests for 'Create an order'
    """

    @allure.title("TCID-48 Test create paid order guest user")
    @allure.description("Create a 'paid' order with 'guest' customer")
    @pytest.mark.tcid48
    def test_create_paid_order_guest_user(self, my_orders_smoke_setup) -> None:
        """
        Create a 'paid' order with 'guest' customer
        """

        with allure.step(f"Make the call 'Create an order'"):
            orders_helper = my_orders_smoke_setup['orders_helper']
            customer_id = 0
            product_id = my_orders_smoke_setup['product_db_id']
            payload = {"line_items": [
                {
                    "product_id": product_id,
                    "quantity": generate_random_number_integer()
                }
            ]}
            order_api = orders_helper.call_create_order(payload_add=payload)
        with allure.step(f"Verify response"):
            products_id_expected = [{'product_id': product_id}]
            orders_helper.verify_order_is_created(order_api, customer_id, products_id_expected, payload)

    @allure.title("TCID-49 Test create paid order new created customer")
    @allure.description("Create a 'paid' order with 'guest' customer")
    @pytest.mark.tcid49
    def test_create_paid_order_new_created_customer(self, my_orders_smoke_setup) -> None:
        """
        Create a 'paid' order with 'new created' customer
        """

        with allure.step(f"Make the call 'Create a customer'"):
            customers_helper = CustomersHelper()
            customer_api = customers_helper.call_create_customer()
            customer_api_id = customer_api['id']
        with allure.step(f"Make the call 'Create an order'"):
            product_id = my_orders_smoke_setup['product_db_id']
            orders_helper = my_orders_smoke_setup['orders_helper']
            payload = {"line_items": [
                {
                    "product_id": product_id,
                    "quantity": generate_random_number_integer()
                }
            ],
                "customer_id": customer_api_id
            }
            order_api = orders_helper.call_create_order(payload_add=payload)
        with allure.step(f"Verify response"):
            products_id_expected = [{'product_id': product_id}]
            orders_helper.verify_order_is_created(order_api, customer_api_id, products_id_expected, payload)

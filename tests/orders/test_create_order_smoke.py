import pytest

from src.helpers.customers_helper import CustomersHelper
from src.utilities.generic_utilities import *


pytestmark = [pytest.mark.orders, pytest.mark.smoke]


@pytest.mark.tcid48
def test_create_paid_order_guest_user(my_orders_smoke_setup):
    # Create helper objects
    orders_helper = my_orders_smoke_setup['orders_helper']

    customer_id = 0
    product_id = my_orders_smoke_setup['product_database_id']

    # Make the call
    payload = {"line_items": [
        {
            "product_id": product_id,
            "quantity": generate_random_number_integer()
        }
    ]}
    order_response = orders_helper.create_order(payload_additional=payload)

    # Verify response
    products_expected = [{'product_id': product_id}]
    orders_helper.verify_order_is_created(order_response, customer_id, products_expected)


@pytest.mark.tcid49
def test_create_paid_order_new_created_customer(my_orders_smoke_setup):
    # Create helper objects
    orders_helper = my_orders_smoke_setup['orders_helper']
    customers_helper = CustomersHelper()

    # Make the call
    customer_response = customers_helper.create_customer()
    customer_response_id = customer_response['id']
    product_id = my_orders_smoke_setup['product_database_id']

    payload = {"line_items": [
        {
            "product_id": product_id,
            "quantity": generate_random_number_integer()
        }
    ],
        "customer_id": customer_response_id
    }
    order_response = orders_helper.create_order(payload_additional=payload)

    # Verify response
    expected_products = [{'product_id': product_id}]
    orders_helper.verify_order_is_created(order_response, customer_response_id, expected_products)

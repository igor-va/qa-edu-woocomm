import pytest

from src.helpers.orders_helper import OrdersHelper


pytestmark = [pytest.mark.orders, pytest.mark.regression]


@pytest.mark.skip("No understanding how the final price is calculated, taking into account the discount")
@pytest.mark.tcid60
def test_apply_valid_coupon_to_order(my_setup_teardown):
    """
    Validates when x% coupon is applied to an order, the 'total' amount is reduced by x%
    """

    # Create payload and make call to create order
    order_helper = OrdersHelper()
    payload = {
        "line_items": [{"product_id": my_setup_teardown['product_id'], "quantity": 2}],
        "coupon_lines": [{"code": my_setup_teardown['coupon_code']}],
        "shipping_lines": [{"method_id": "flat_rate", "method_title": "Flat Rate", "total": "0.00"}]
        }
    order_response = order_helper.call_create_order(payload_add=payload)

    # Calculate expected total price based on coupon and product price
    expected_total = float(my_setup_teardown['product_price']) * (float(my_setup_teardown['discount_pct'])/100)
    expected_total = round(expected_total, 2)

    # Get total from order response and verify
    total = round(float(order_response['total']), 2)

    # Verify 'total' is update in database
    assert total == expected_total, \
        f"Order total is not reduced after applying 50% coupon, expected cost '{expected_total}', actual: '{total}'."

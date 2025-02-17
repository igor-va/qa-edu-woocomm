import pytest
import random

from src.dao.products_dao import ProductsDAO
from src.helpers.orders_helper import OrdersHelper
from src.helpers.products_helper import ProductsHelper


@pytest.fixture(scope='module')
def my_orders_smoke_setup():
    # Create helper objects
    products_dao = ProductsDAO()
    orders_helper = OrdersHelper()

    # Get random product from db
    product_database = products_dao.get_random_products(1)
    product_database_id = product_database[0]['ID']

    setup_info = {'product_database_id': product_database_id,
                  'orders_helper': orders_helper}

    return setup_info


@pytest.fixture(scope='module')
def my_setup_teardown():
    # Hard code 50% coupon
    coupon_code = 'qutgwtcid37'
    discount_pct = '84.00'

    # Get a random product for order
    products_response = ProductsHelper().call_list_products_with_filter()
    product_response = random.choice(products_response)

    # Generate some data
    setup_info = dict()
    setup_info['order_helper'] = OrdersHelper()
    setup_info['coupon_code'] = coupon_code
    setup_info['discount_pct'] = discount_pct
    setup_info['product_id'] = product_response['id']
    setup_info['product_price'] = product_response['price']

    return setup_info

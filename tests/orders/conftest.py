import pytest

from src.dao.products_dao import ProductsDAO
from src.helpers.orders_helper import OrdersHelper


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

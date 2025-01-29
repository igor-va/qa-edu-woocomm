import pytest

from src.utilities.requests_utility import RequestsUtility
from src.dao.products_dao import ProductsDAO
from src.helpers.products_helper import ProductsHelper
from src.endpoints.endpoints import Endpoints


pytestmark = [pytest.mark.products, pytest.mark.smoke]


@pytest.mark.tcid24
def test_get_all_products():
    # Make the call
    requests_utility = RequestsUtility()
    products_response = requests_utility.get(Endpoints.products)

    # Verify response is not empty
    assert products_response, f"Get all products endpoint returned nothing."


@pytest.mark.tcid25
def test_get_product_by_id():
    # Get a random product from db
    product_database = ProductsDAO().get_random_product_from_db()
    product_database_id = product_database[0]['ID']
    product_database_name = product_database[0]['post_title']

    # Make the call
    product_helper = ProductsHelper()
    product_response = product_helper.get_product_by_id(product_database_id)
    product_response_name = product_response['name']

    # Verify the response
    assert product_database_name == product_response_name, \
        f"Get product by id returned wrong product, DB ID get '{product_database_id}',  \
        DB name get {product_database_name}, API name returned {product_response_name}"

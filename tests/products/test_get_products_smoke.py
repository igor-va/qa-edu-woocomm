import pytest
import allure

from src.dao.products_dao import ProductsDAO
from src.helpers.products_helper import ProductsHelper


pytestmark = [pytest.mark.products, pytest.mark.smoke, pytest.mark.api]


@allure.feature("Products")
@allure.story("List all products")
@allure.title("Test get all products")
@allure.description("Verify 'GET /products' does not return empty")
@pytest.mark.tcid24
def test_get_all_products():
    """Verify 'GET /products' does not return empty"""

    with allure.step(f"Make the call 'List all products'"):
        products_helper = ProductsHelper()
        product_api = products_helper.call_list_all_products()

    with allure.step(f"Verify the response is not empty"):
        assert product_api, f"Call 'List all products' returned nothing."


@allure.feature("Products")
@allure.story("Retrieve a product")
@allure.title("Test get product by id")
@allure.description("Verify 'GET /products/id' returns a product with the given id")
@pytest.mark.tcid25
def test_get_product_by_id():
    """Verify 'GET /products/id' returns a product with the given id"""

    # Get a random product from db
    product_database = ProductsDAO().get_random_products()
    product_database_id = product_database[0]['ID']
    product_database_name = product_database[0]['post_title']

    # Make the call
    products_helper = ProductsHelper()
    product_response = products_helper.get_product_by_id(product_database_id)
    product_response_name = product_response['name']

    # Verify the response
    assert product_database_name == product_response_name, \
        f"Get product by id returned wrong product, DB ID get '{product_database_id}',  \
        DB name get {product_database_name}, API name returned {product_response_name}"

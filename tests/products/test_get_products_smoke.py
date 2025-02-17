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
def test_get_all_products() -> None:
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
def test_get_product_by_id() -> None:
    """Verify 'GET /products/id' returns a product with the given id"""

    with allure.step(f"Get a random product from DB"):
        product_db = ProductsDAO().get_random_products()
        product_db_id = product_db[0]['ID']
        product_db_name = product_db[0]['post_title']
    with allure.step(f"Make the call 'Retrieve a product'"):
        products_helper = ProductsHelper()
        product_api = products_helper.call_retrieve_product_by_id(product_db_id)
        product_api_name = product_api['name']
    with allure.step(f"Verify the response"):
        assert product_db_name == product_api_name, \
            f"Get product by id returned wrong product, expected {product_db_name}, actual {product_api_name}."

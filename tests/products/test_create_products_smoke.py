import pytest
import allure

from src.utilities.generic_utilities import *
from src.helpers.products_helper import ProductsHelper
from src.dao.products_dao import ProductsDAO


pytestmark = [pytest.mark.products, pytest.mark.smoke, pytest.mark.api]


@allure.feature("Products")
@allure.story("Create a product")
@allure.title("Test create one simple product")
@allure.description("Verify 'POST /products' create a one simple product")
@pytest.mark.tcid26
def test_create_one_simple_product() -> None:
    """Verify 'POST /products' create a one simple product"""

    with allure.step(f"Generate some test data"):
        payload = dict()
        payload_name = generate_random_string()
        payload['name'] = payload_name
        payload['type'] = "simple"
        payload['regular_price'] = generate_random_number_float()
    with allure.step(f"Make the call 'Create a product'"):
        product_api = ProductsHelper().call_create_product(payload)
    with allure.step(f"Verify the response is not empty"):
        assert product_api, \
            f"Call 'Create a product' is empty, 'payload' should be '{payload}'."
    with allure.step(f"Verify the response has returned the correct 'name'"):
        product_api_name = product_api['name']
        assert product_api_name == payload_name, \
            f"Call 'Create a product' return unexpected 'name', expected '{payload_name}', actual '{product_api_name}'."
    with allure.step(f"Get product from DB by 'id'"):
        product_db = ProductsDAO().get_product_by_id(product_api['id'])
    with allure.step(f"Verify the product exists in DB"):
        product_db_name = product_db[0]['post_title']
        assert product_db_name == payload_name, \
            f"Title in DB does not match title in API, expected '{payload_name}', actual '{product_db_name}'."

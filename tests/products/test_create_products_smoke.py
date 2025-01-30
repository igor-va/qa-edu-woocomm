import pytest

from src.utilities.generic_utilities import *
from src.helpers.products_helper import ProductsHelper
from src.dao.products_dao import ProductsDAO


pytestmark = [pytest.mark.products, pytest.mark.smoke]


@pytest.mark.tcid26
def test_create_one_simple_product():
    # Generate some data
    payload = dict()
    payload['name'] = generate_random_string()
    payload['type'] = "simple"
    payload['regular_price'] = generate_random_number_float()

    # Make the call
    product_response = ProductsHelper().call_create_product(payload)

    # Verify the response is not empty
    assert product_response, f"Create product api response is empty, payload should be {payload}"
    assert product_response['name'] == payload['name'], f"Create product api call response has \
        unexpected name, expected {payload['name']}, but returned {product_response['name']}"

    # Verify the product exists in db
    product_response_id = product_response['id']
    product_database = ProductsDAO().get_product_by_id(product_response_id)
    product_database_name = product_database[0]['post_title']
    assert payload['name'] == product_database_name, \
        f"Title in DB does not match title in API, DB get {product_database_name}, API returned {payload['name']}."

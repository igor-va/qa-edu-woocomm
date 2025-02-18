import pytest
import allure
import random

from src.helpers.products_helper import ProductsHelper
from src.dao.products_dao import ProductsDAO
from src.utilities.generic_utilities import *


pytestmark = [pytest.mark.products, pytest.mark.regression]


@allure.feature("Products")
@allure.story("Update a product")
@allure.title("TCID-61 Test update regular price should update price")
@allure.description("Verifies updating the 'regular_price' field should automatically update the 'price' field")
@pytest.mark.tcid61
def test_update_regular_price_should_update_price() -> None:
    """
    Verifies updating the 'regular_price' field should automatically update the 'price' field.
    For this test the 'sale_price' of the product must be empty.
    If product has 'sale_price', updating the 'regular_price' does not update the 'price'.
    So get a bunch of products and loop until you find one that is not 'on_sale'.
    If all in the list are 'on_sale' then take random one and update the 'sale_price'.
    """

    with allure.step(f"Find random product where 'sale_price' field must be empty"):
        products_helper = ProductsHelper()
        products_dao = ProductsDAO()
        products_random = products_dao.get_random_products(5)
        for product in products_random:
            # Get random product if product 'sale_price' be empty
            product_id = product['ID']
            product_api = products_helper.call_retrieve_product_by_id(product_id)
            if product_api['on_sale']:
                continue
            else:
                break
        else:
            # Take random product and make it not 'on_sale' by setting 'sale_price'=''
            product_random = random.choice(products_random)
            product_id = product_random['ID']
            payload = dict()
            payload['sale_price'] = ''
            products_helper.call_update_product(product_id, payload)
    with allure.step(f"Make the update product 'regular_price' field"):
        new_price = generate_random_number_float()
        payload = dict()
        payload['regular_price'] = new_price
        product_api = products_helper.call_update_product(product_id, payload)
    with allure.step(f"Verify the 'price' and 'regular_price' has updated and 'sale_price' is not updated"):
        assert product_api['price'] == new_price, \
            f"Updating 'regular_price' did not update 'price', expected {new_price}, actual {product_api['price']}."
        assert product_api['regular_price'] == new_price, \
            f"Updating 'regular_price' did not update, expected {new_price}, actual {product_api['regular_price']}."
        assert product_api['sale_price'] == '', \
            f"The 'sale_price' field should be empty, actual {product_api['sale_price']}."
    with allure.step(f"Get the product after the update and verify response"):
        product_api = products_helper.call_retrieve_product_by_id(product_id)
        assert product_api['price'] == new_price, \
            f"Updating 'regular_price' did not update 'price', expected {new_price}, actual {product_api['price']}."
        assert product_api['regular_price'] == new_price, \
            f"Updating 'regular_price' did not update, expected {new_price}, actual {product_api['regular_price']}."
        assert product_api['sale_price'] == '', \
            f"The 'sale_price' field should be empty, actual {product_api['sale_price']}."


@pytest.mark.tcid65
def test_adding_sale_price_should_set_on_sale_flag_true():
    """
    When the 'sale_price' of a product is updated, then it should set the field 'on_sale'=True
    """

    # Create helper objects
    products_helper = ProductsHelper()
    products_dao = ProductsDAO()

    # First get a product from db that is not 'on_sale'
    product_database = products_dao.get_random_products_that_are_not_on_sale(1)
    product_database_id = product_database[0]['ID']

    # Check the 'on_sale' field is 'False' to start with
    product_response_before = products_helper.call_retrieve_product_by_id(product_database_id)
    assert not product_response_before['on_sale'], \
        f"Getting test data with 'on_sale'='False' but got 'True', unable to use this product for test."

    # Update the 'sale_price' of the product
    regular_price = product_response_before['regular_price']
    if regular_price == "":
        sale_price = 10
    else:
        sale_price = float(regular_price) * 0.75  # sale is 75% of original
    payload = dict()
    payload['sale_price'] = str(sale_price)
    products_helper.call_update_product(product_database_id, payload=payload)

    # Get the product 'sale_price' and verify is updated
    product_response_after = products_helper.call_retrieve_product_by_id(product_database_id)
    assert product_response_after['sale_price'] == str(sale_price), \
        f"Updated product 'sale_price' but value did not update, product id '{product_database_id}', \
        expected 'sale_price' '{sale_price}', but actual 'sale_price' '{product_response_after['sale_price']}'."


@pytest.mark.tcid63
@pytest.mark.tcid64
def test_update_on_sale_field_buy_updating_sale_price():
    """
    Two test case.
    First case update the 'sale_price'>0 and verify the field changes to 'on_sale'=True.
    Second case update the 'sale_price'="" and verify the field changes to 'on_sale'=False.
    """

    # Create helper objects
    products_helper = ProductsHelper()

    # Create product for the tests and
    regular_price = generate_random_number_float()
    payload = dict()
    payload['name'] = generate_random_string()
    payload['type'] = 'simple'
    payload['regular_price'] = regular_price
    product_response_before = products_helper.call_create_product(payload)
    product_response_id = product_response_before['id']

    # Verify the product has 'on_sale'=False
    assert not product_response_before['on_sale'], \
        f"Newly created product should not have 'on_sale'=True, product id '{product_response_id}'."
    assert not product_response_before['sale_price'], \
        f"Newly created product should not have value for 'sale_price' field."

    # For 'tcid-63' update the 'sale_price' and verify the 'on_sale' is set to True
    payload = dict()
    payload['sale_price'] = str(float(regular_price) * .75)
    products_helper.call_update_product(product_response_id, payload)
    product_response_after = products_helper.call_retrieve_product_by_id(product_response_id)
    assert product_response_after['on_sale'], \
        f"Updated 'sale_price' of product, but the 'on_sale' did not set to 'True', \
        product id '{product_response_id}'."

    # For 'tcid-64' update the 'sale_price' to empty string and verify the 'on_sale' is set to False
    payload = dict()
    payload['sale_price'] = ''
    products_helper.call_update_product(product_response_id, payload)
    product_response_after = products_helper.call_retrieve_product_by_id(product_response_id)
    assert not product_response_after['on_sale'], \
        f"Updated 'sale_price'='' of product, but the 'on_sale' did not set to 'False', \
        product id '{product_response_id}'."

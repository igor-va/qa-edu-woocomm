import pytest
import allure
import random

from src.helpers.products_helper import ProductsHelper
from src.dao.products_dao import ProductsDAO
from src.utilities.generic_utilities import *


pytestmark = [pytest.mark.products, pytest.mark.regression]


@allure.feature("Products")
@allure.story("Update a product")
class TestUpdateProducts(object):
    """
    Tests for 'Update a product'
    """

    @allure.title("TCID-61 Test update regular price should update price")
    @allure.description("Verifies updating the 'regular_price' field should automatically update the 'price' field")
    @pytest.mark.tcid61
    def test_update_regular_price_should_update_price(self) -> None:
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
        with allure.step(f"Verify product after the update"):
            product_api = products_helper.call_retrieve_product_by_id(product_id)
            assert product_api['price'] == new_price, \
                f"Updating 'regular_price' did not update 'price', expected {new_price}, actual {product_api['price']}."
            assert product_api['regular_price'] == new_price, \
                f"Updating 'regular_price' did not update, expected {new_price}, actual {product_api['regular_price']}."
            assert product_api['sale_price'] == '', \
                f"The 'sale_price' field should be empty, actual {product_api['sale_price']}."

    @allure.title("TCID-65 Test update sale price should set flag on sale true")
    @allure.description("Verify updating 'sale_price' updates the 'on_price' field")
    @pytest.mark.tcid65
    def test_update_sale_price_should_set_flag_on_sale_true(self):
        """
        When the 'sale_price' of a product is updated, then it should set the field 'on_sale'=True
        """

        with allure.step(f"Get a product from DB that is not 'on_sale'"):
            products_dao = ProductsDAO()
            product_db = products_dao.get_random_products_that_are_not_on_sale(1)
            product_db_id = product_db[0]['ID']
        with allure.step(f"Check the 'on_sale' field is 'False' to start with"):
            products_helper = ProductsHelper()
            product_api = products_helper.call_retrieve_product_by_id(product_db_id)
            assert not product_api['on_sale'], \
                f"Getting test data with 'on_sale'='False', but got 'True', unable to use this product for test."
        with allure.step(f"Update the 'sale_price' of the product"):
            product_api_regular_price = product_api['regular_price']
            payload = dict()
            if product_api_regular_price == "":
                regular_price = generate_random_number_float(min_value=10, max_value=20)
                sale_price = float(regular_price) * 0.75
                payload['regular_price'] = str(regular_price)
                payload['sale_price'] = str(sale_price)
            else:
                sale_price = float(product_api_regular_price) * 0.75  # sale is 75% of original
                payload['sale_price'] = str(sale_price)
            products_helper.call_update_product(product_db_id, payload=payload)
        with allure.step(f"Verify the product 'sale_price' field is updated"):
            product_api = products_helper.call_retrieve_product_by_id(product_db_id)
            product_api_sale_price = product_api['sale_price']
            assert product_api_sale_price == str(sale_price), \
                f"Field 'sale_price' did not update, expected {sale_price}', actual {product_api_sale_price}."

    @allure.title("TCID-63 Test update sale price greater zero should set flag on sale true")
    @allure.description("Verify update 'sale_price'>'0' will set field 'on_sale'=True")
    @pytest.mark.tcid63
    def test_update_sale_price_greater_zero_should_set_flag_on_sale_true(self):
        """
        Verify update 'sale_price'>'0' will set field 'on_sale'=True
        """

        with allure.step(f"Create product for the tests"):
            products_helper = ProductsHelper()
            regular_price = generate_random_number_float()
            payload = dict()
            payload['name'] = generate_random_string()
            payload['type'] = 'simple'
            payload['regular_price'] = regular_price
            product_api = products_helper.call_create_product(payload)
            product_api_id = product_api['id']
        with allure.step(f"Verify the product has 'on_sale'=False"):
            assert not product_api['on_sale'], \
                f"Newly created product should not have 'on_sale'=True, product id {product_api_id}."
            assert not product_api['sale_price'], \
                f"Newly created product should not have value for 'sale_price' field."
        with allure.step(f"Update the 'sale_price'"):
            payload = dict()
            payload['sale_price'] = str(float(regular_price) * 0.75)
            products_helper.call_update_product(product_api_id, payload)
            product_api = products_helper.call_retrieve_product_by_id(product_api_id)
        with allure.step(f"Verify the 'on_sale' is set True"):
            assert product_api['on_sale'], \
                f"Updated 'sale_price' of product, but the 'on_sale' did not set True, product id {product_api_id}."

    @allure.title("TCID-64 Test update sale price empty should set flag on sale false")
    @allure.description("Verify update the 'sale_price' to empty string and verify the 'on_sale' is set to False")
    @pytest.mark.tcid64
    def test_update_sale_price_empty_should_set_flag_on_sale_false(self):
        """
        Verify update the 'sale_price' to empty string and verify the 'on_sale' is set to False
        """

        with allure.step(f"Create product for the tests"):
            products_helper = ProductsHelper()
            regular_price = generate_random_number_float()
            sale_price = str(float(regular_price) * 0.75)
            payload = dict()
            payload['name'] = generate_random_string()
            payload['type'] = 'simple'
            payload['regular_price'] = regular_price
            payload['sale_price'] = sale_price
            product_api = products_helper.call_create_product(payload)
            product_api_id = product_api['id']
        with allure.step(f"Verify the product has 'on_sale'=True"):
            assert product_api['on_sale'], \
                f"Newly created product should not have 'on_sale'=False, product id {product_api_id}."
            assert product_api['sale_price'] == sale_price, \
                f"Return unexpected 'sale_price', expected {sale_price}, actual {product_api['sale_price']}."
        with allure.step(f"Update the 'sale_price' to empty string"):
            payload = dict()
            payload['sale_price'] = ''
            products_helper.call_update_product(product_api_id, payload)
            product_api = products_helper.call_retrieve_product_by_id(product_api_id)
        with allure.step(f"Verify the 'on_sale' is set to False"):
            assert not product_api['on_sale'], \
                f"Field 'on_sale' did not set to 'False', product id {product_api_id}."
            assert product_api['sale_price'] == '', \
                f"Return unexpected 'sale_price', expected '', actual {product_api['sale_price']}."

import pytest
import allure
from datetime import datetime, timedelta

from src.helpers.products_helper import ProductsHelper
from src.dao.products_dao import ProductsDAO


pytestmark = [pytest.mark.products, pytest.mark.regression]


@allure.feature("Products")
@allure.story("List all products")
class TestListProductsWithFilter(object):
    """Tests for retrieve products with filter"""

    @allure.title("Test get products with filter after")
    @allure.description("Verify 'GET /products' with filter 'after'")
    @pytest.mark.tcid51
    def test_get_products_with_filter_after(self) -> None:
        """Verify 'GET /products' with filter 'after'"""

        with allure.step(f"Generate test data"):
            payload = dict()
            date_after = (datetime.now().replace(microsecond=0) - timedelta(days=300)).isoformat()
            payload['after'] = date_after
        with allure.step(f"Make the call 'List all products' with filter 'after'"):
            products_api = ProductsHelper().call_list_products_with_filter(payload)
        with allure.step(f"Verify the response is not empty"):
            assert products_api, f"Empty response for cal 'List all products' with filter after"
        with allure.step(f"Get data from DB with filter 'after'"):
            products_db = ProductsDAO().get_products_created_after_given_date(date_after)
        with allure.step(f"Verify length API match DB"):
            assert len(products_api) == len(products_db), \
                f"List products with filter 'after' returned unexpected number of products, " \
                f"expected {len(products_db)}, actual {len(products_api)}."
        with allure.step(f"Verify that API and DB 'ID' are the same"):
            products_api_id = [i['id'] for i in products_api]
            products_db_id = [i['ID'] for i in products_db]
            products_id_diff = list(set(products_api_id) - set(products_db_id))
            assert not products_id_diff, f"Product 'ID' in API mismatch in DB."

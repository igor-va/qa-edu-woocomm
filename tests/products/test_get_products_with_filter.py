import pytest
from datetime import datetime, timedelta

from src.helpers.products_helper import ProductsHelper
from src.dao.products_dao import ProductsDAO


@pytest.mark.regression
class TestListProductsWithFilter(object):

    @pytest.mark.tcid51
    def test_list_products_with_filter_after(self):
        # Create data
        payload = dict()
        after_created_date = (datetime.now().replace(microsecond=0) - timedelta(days=300)).isoformat()
        payload['after'] = after_created_date

        # Make the call and verify response is not empty
        products_response = ProductsHelper().call_list_products(payload)
        assert products_response, f"Empty response for 'list products with filer"

        # Get data from db
        products_database = ProductsDAO().get_products_created_after_given_date(after_created_date)

        # Verify length response match db
        assert len(products_response) == len(products_database), \
            f"List products with filter 'after' returned unexpected number of products, \
            expected {len(products_database)}, but actual {len(products_response)}."

        # Verify ids response match db
        products_response_id = [i['id'] for i in products_response]
        products_database_id = [i['ID'] for i in products_database]
        products_id_diff = list(set(products_response_id) - set(products_database_id))
        assert not products_id_diff, f"List products with filter, product ids in response mismatch in db."

import logging as logger
import pytest

from src.utilities.requestsUtility import RequestsUtility
from src.endpoints.endpoints import Endpoints


@pytest.mark.customers
@pytest.mark.tcid30
def test_get_all_customers():

    request_helper = RequestsUtility()
    response_api_info = request_helper.get(Endpoints.customers)

    assert response_api_info, f"Response of list all customers is empty."

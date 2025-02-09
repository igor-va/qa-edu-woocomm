import logging as logger
import pytest

from src.utilities.requests_utility import RequestsUtility
from src.endpoints.endpoints import Endpoints


pytestmark = [pytest.mark.customers, pytest.mark.smoke]


@pytest.mark.tcid30
def test_get_all_customers():
    # Make the call
    requests_helper = RequestsUtility()
    customer_response = requests_helper.get(Endpoints.customers)

    # Verify response is not empty
    assert customer_response, f"Response of list all customers is empty."

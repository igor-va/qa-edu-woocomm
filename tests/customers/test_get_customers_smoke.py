import pytest
import allure

from src.helpers.customers_helper import CustomersHelper


pytestmark = [pytest.mark.customers, pytest.mark.smoke]


@allure.feature("Customers")
@allure.story("List all customers")
@allure.title("TCID-30 Test get all customers")
@allure.description("Verify 'GET /customers' lists all users")
@pytest.mark.tcid30
def test_get_all_customers() -> None:
    """
    Verify 'GET /customers' lists all users
    """

    with allure.step(f"Make the call 'List all customers'"):
        requests_helper = CustomersHelper()
        customer_api = requests_helper.call_list_all_customers()
    with allure.step(f"Verify response is not empty"):
        assert customer_api, f"Response of list all customers is empty."

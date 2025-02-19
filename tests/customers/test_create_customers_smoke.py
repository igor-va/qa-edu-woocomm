import pytest
import allure

from src.utilities.generic_utilities import *
from src.helpers.customers_helper import CustomersHelper
from src.dao.customers_dao import CustomersDAO


pytestmark = [pytest.mark.customers, pytest.mark.smoke]


@allure.feature("Customers")
@allure.story("Create a customer")
class TestCreateCustomer(object):
    """
    Tests for 'Create a customer'
    """

    @allure.title("TCID-29 Test create customer only email password")
    @allure.description("Verify 'POST /customers' creates user with email and password only")
    @pytest.mark.tcid29
    def test_create_customer_only_email_password(self) -> None:
        """
        Verify 'POST /customers' creates user with email and password only
        """

        with allure.step(f"Get 'email' and 'password'"):
            email = generate_random_email()
            password = generate_random_password()
        with allure.step(f"Make the call 'Create a customer'"):
            customers_helper = CustomersHelper()
            customer_api = customers_helper.create_customer(email=email, password=password)
        with allure.step(f"Verify 'email' and 'first_name' in the response"):
            assert customer_api['email'] == email, \
                f"Call 'Create a customer' return wrong 'email', expected {email}, actual {customer_api['email']}."
            assert customer_api['first_name'] == '', \
                f"Call 'Create a customer' return value for 'first_name', but it should be empty."
        with allure.step(f"Verify customer is created in DB"):
            customers_dao = CustomersDAO()
            customer_db = customers_dao.get_customer_by_email(email)
            customer_api_id = customer_api['id']
            customer_db_id = customer_db[0]['ID']
            assert customer_api_id == customer_db_id, \
                f"API 'id' not same as DB 'ID, API 'id' {customer_api_id}, DB 'ID' {customer_db_id}."

    @allure.title("TCID-47 Test create customer fail for existing email")
    @allure.description("Verify 'create customer' fail if email exists")
    @pytest.mark.tcid47
    def test_create_customer_fail_for_existing_email(self) -> None:
        """
        Verify 'create customer' fail if email exists
        """

        with allure.step(f"Get existing email from DB"):
            customers_dao = CustomersDAO()
            customer_db = customers_dao.get_random_customer_from_db()
            customer_db_email = customer_db[0]['user_email']
        with allure.step(f"Make the call 'Create a customer' with existing email"):
            customer_helper = CustomersHelper()
            customer_api = customer_helper.create_customer(email=customer_db_email, exp_st_code=400)
        with allure.step(f"Verify customer is not created in DB"):
            assert customer_api['code'] == 'registration-error-email-exists', \
                f"Create customer with existing user error 'code' is not correct."
            assert customer_api['message'] == (f"An account is already registered with {customer_db_email}. "
                                               f"Please log in or use a different email address."), \
                f"Create customer with existing user error 'message' is not correct."

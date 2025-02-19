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

    @pytest.mark.tcid47
    def test_create_customer_fail_for_existing_email(self):
        # Get existing email from db
        customers_dao = CustomersDAO()
        customer_exist = customers_dao.get_random_customer_from_db()
        customer_email = customer_exist[0]['user_email']

        # Call the api with existing email
        customer_helper = CustomersHelper()
        customer_response = customer_helper.create_customer(email=customer_email, exp_st_code=400)

        # Verify customer is not created in database
        assert customer_response['code'] == 'registration-error-email-exists', \
            f"Create customer with existing user error 'code' is not correct, \
            should be: 'registration-error-email-exists', but returned '{customer_response['code']}'."
        assert customer_response['message'] == \
            f"An account is already registered with {customer_email}. Please log in or use a different email address.", \
            f"Create customer with existing user error 'message' is not correct."

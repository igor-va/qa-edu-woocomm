import pytest
import logging as logger

from src.utilities.generic_utilities import generate_random_email_and_password
from src.helpers.customers_helper import CustomersHelper
from src.dao.customers_dao import CustomersDAO


pytestmark = [pytest.mark.customers, pytest.mark.smoke]


@pytest.mark.tcid29
def test_create_customer_only_email_password():
    logger.info("TEST: Create new customer with email and password only.")

    # Get 'email' and 'password'
    random_info = generate_random_email_and_password()
    email = random_info['email']
    password = random_info['password']

    # Make the call
    customers_helper = CustomersHelper()
    customer_response = customers_helper.create_customer(email=email, password=password)

    # Verify 'email' and 'first name' in the response
    assert customer_response['email'] == email, \
        f"Create customer api return wrong email, email should be '{email}', but returned '{customer_response['email']}'."
    assert customer_response['first_name'] == '', \
        f"Create customer api returned value for 'first_name', but it should be empty."

    # Verify customer is created in database
    customers_dao = CustomersDAO()
    customer_database = customers_dao.get_customer_by_email(email)
    customer_response_id = customer_response['id']
    customer_database_id = customer_database[0]['ID']
    assert customer_response_id == customer_database_id, \
        f"Create customer response 'id' not same as 'ID in database, \
        'id' should be '{customer_response_id}, but 'ID' in database '{customer_database_id}'."


@pytest.mark.tcid47
def test_create_customer_fail_for_existing_email():
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

import pytest
import logging as logger

from src.utilities.genericUtilities import generate_random_email_and_password
from src.helpers.customers_helper import CustomerHelper
from src.dao.customers_dao import CustomersDAO


@pytest.mark.customers
@pytest.mark.tcid29
def test_create_customer_only_email_password():

    logger.info("TEST: Create new customer with email and password only.")

    # Get 'email' and 'password'
    random_info = generate_random_email_and_password()
    email = random_info['email']
    password = random_info['password']

    # Make the call
    customer_helper = CustomerHelper()
    customer_api_info = customer_helper.create_customer(email=email, password=password)

    # Verify 'email' and 'first name' in the response
    assert customer_api_info['email'] == email, \
        f"Create customer api return wrong email, email should be '{email}', but returned '{customer_api_info['email']}'."
    assert customer_api_info['first_name'] == '', \
        f"Create customer api returned value for 'first_name', but it should be empty."

    # Verify customer is created in database
    customer_dao = CustomersDAO()
    customer_dao_info = customer_dao.get_customer_by_email(email)
    customer_id_api = customer_api_info['id']
    customer_id_db = customer_dao_info[0]['ID']
    assert customer_id_api == customer_id_db, \
        f"Create customer response 'id' not same as 'ID in database, \
        'id' should be '{customer_id_api}, but 'ID' in database '{customer_id_db}'."


@pytest.mark.customers
@pytest.mark.tcid47
def test_create_customer_fail_for_existing_email():

    # Get existing email from db
    customer_dao = CustomersDAO()
    customer_exist = customer_dao.get_random_customer_from_db()
    customer_email = customer_exist[0]['user_email']

    # Call the api with existing email
    customer_helper = CustomerHelper()
    customer_api_info = customer_helper.create_customer(email=customer_email, exp_st_code=400)

    # Verify customer is not created in database
    assert customer_api_info['code'] == 'registration-error-email-exists', \
        f"Create customer with existing user error 'code' is not correct, \
        should be: 'registration-error-email-exists', but returned '{customer_api_info['code']}'."
    assert customer_api_info['message'] == \
        f"An account is already registered with {customer_email}. Please log in or use a different email address.", \
        f"Create customer with existing user error 'message' is not correct."

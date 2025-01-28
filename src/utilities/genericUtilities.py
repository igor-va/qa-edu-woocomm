import logging as logger
import random
import string
from faker import Faker


def generate_random_email_and_password() -> dict:
    logger.debug("Generating random email and password.")

    fake = Faker()
    email = fake.email()
    password = fake.password(length=20)
    random_info = {'email': email, 'password': password}

    logger.debug(f"Randomly generated email and password: {random_info}")

    return random_info


def generate_random_string(length=10, prefix=None, suffix=None):

    random_string = ''.join(random.choices(string.ascii_lowercase, k=length))

    if prefix:
        random_string = prefix + random_string
    if suffix:
        random_string = random_string + suffix

    return random_string


def generate_random_coupon_code(suffix=None, length=10):

    code = ''.join(random.choices(string.ascii_uppercase, k=length))
    if suffix:
        code += suffix

    return code

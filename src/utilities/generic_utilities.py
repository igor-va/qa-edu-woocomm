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


def generate_random_string() -> str:
    fake = Faker()
    random_string = fake.word(part_of_speech="noun").title()
    return random_string


def generate_random_number_float() -> str:
    fake = Faker()
    number = fake.pyfloat(min_value=10, max_value=1000, right_digits=2)
    return str(number)


def generate_random_number_integer() -> str:
    fake = Faker()
    number = fake.random_int(min=1, max=20)
    return str(number)


def generate_random_coupon_code(suffix=None, length=10):
    code = ''.join(random.choices(string.ascii_uppercase, k=length))
    if suffix:
        code += suffix
    return code

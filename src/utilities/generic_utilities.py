import string
from faker import Faker


def generate_random_email() -> str:
    """
    Generate random email
    """

    fake = Faker()
    email = fake.email()
    return email


def generate_random_password() -> str:
    """
    Generate random password
    """

    fake = Faker()
    password = fake.password(length=20)
    return password


def generate_random_string() -> str:
    """
    Generate random string
    """

    fake = Faker()
    random_string = fake.word(part_of_speech="noun").title()
    return random_string


def generate_random_sentence() -> str:
    fake = Faker()
    random_sentence = fake.sentence()
    return random_sentence


def generate_random_number_float(min_value=10, max_value=1000, round_value=2) -> str:
    """
    Generate random number float
    """

    fake = Faker()
    number = fake.pyfloat(min_value=min_value, max_value=max_value, right_digits=round_value)
    number = f"{number:.2f}"
    return number


def generate_random_number_integer() -> str:
    """
    Generate random number integer
    """
    fake = Faker()
    number = fake.random_int(min=1, max=20)
    return str(number)


def generate_random_coupon_code():
    fake = Faker()
    coupon_code = fake.bothify(text='coupon-####-????', letters=string.ascii_uppercase)
    return coupon_code

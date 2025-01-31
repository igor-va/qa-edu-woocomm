import pytest

from src.helpers.coupons_helper import CouponsHelper


@pytest.fixture(scope='module')
def my_setup():

    setup_info = dict()
    setup_info['coupons_helper'] = CouponsHelper()

    return setup_info

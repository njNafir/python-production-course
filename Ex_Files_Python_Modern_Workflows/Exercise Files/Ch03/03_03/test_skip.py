"""Example of developer & CI tests"""

from os import environ
import pytest

is_ci = 'CI' in environ


def test_developer():
    print('developer test')


@pytest.mark.skipif(not is_ci, reason='not in CI')
def test_ci():
    print('CI test')

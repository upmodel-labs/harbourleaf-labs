from datetime import datetime

import pytest

import bundle


def book(title, fmt, price):
    return {"title": title, "format": fmt, "price": price}


@pytest.fixture
def three_paperbacks():
    return [book("A", "paperback", 12.00), book("B", "paperback", 9.00), book("C", "paperback", 15.00)]


@pytest.fixture
def before_end():
    return datetime(2026, 11, 20, 12, 0, 0)


@pytest.fixture
def after_end():
    return datetime(2026, 12, 1, 0, 0, 1)

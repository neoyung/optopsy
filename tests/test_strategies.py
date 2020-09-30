import os
import pytest

from optopsy.datafeeds import csv_data
from optopsy.strategies import *


def filepath():
    curr_file = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(curr_file, "./test_data/data_full.csv")


@pytest.fixture()
def context():
    return csv_data(filepath())


def test_singles_long_calls(context):
    results = singles_calls(context, side="long")
    assert not results.empty
    assert len(results) == 6


def test_singles_long_puts(context):
    results = singles_puts(context, side="long")
    assert not results.empty
    assert len(results) == 6


def test_singles_short_calls(context):
    results = singles_calls(context, side="short")
    assert not results.empty
    assert len(results) == 6


def test_singles_short_puts(context):
    results = singles_puts(context, side="short")
    assert not results.empty
    assert len(results) == 6
import pytest
import pandas as pd
import datetime as datetime


@pytest.fixture(scope="module")
def data():
    exp_date = datetime.datetime(2015, 10, 30)
    quote_dates = [datetime.datetime(2015, 10, 1), datetime.datetime(2015, 10, 30)]
    cols = [
        "underlying_symbol",
        "underlying_price",
        "option_type",
        "expiration",
        "quote_date",
        "strike",
        "bid",
        "ask",
    ]
    d = [
        ["SPX", 1921.42, "call", exp_date, quote_dates[0], 1910, 50.6, 51.5],
        ["SPX", 1921.42, "call", exp_date, quote_dates[0], 1915, 47.4, 48.4],
        ["SPX", 1921.42, "call", exp_date, quote_dates[0], 1920, 44.5, 45.4],
        ["SPX", 1921.42, "call", exp_date, quote_dates[0], 1925, 41.6, 42.5],
        ["SPX", 1921.42, "put", exp_date, quote_dates[0], 1910, 39.2, 40.1],
        ["SPX", 1921.42, "put", exp_date, quote_dates[0], 1915, 41, 42],
        ["SPX", 1921.42, "put", exp_date, quote_dates[0], 1920, 43, 45],
        ["SPX", 1921.42, "put", exp_date, quote_dates[0], 1925, 45, 46.2],
        ["SPX", 2084.58, "call", exp_date, quote_dates[1], 1910, 160.8, 176.8],
        ["SPX", 2084.58, "call", exp_date, quote_dates[1], 1915, 155.8, 171.8],
        ["SPX", 2084.58, "call", exp_date, quote_dates[1], 1920, 150.8, 166.8],
        ["SPX", 2084.58, "call", exp_date, quote_dates[1], 1925, 145.8, 161.8],
        ["SPX", 2084.58, "put", exp_date, quote_dates[1], 1910, 0, 0],
        ["SPX", 2084.58, "put", exp_date, quote_dates[1], 1915, 0, 0],
        ["SPX", 2084.58, "put", exp_date, quote_dates[1], 1920, 0, 0],
        ["SPX", 2084.58, "put", exp_date, quote_dates[1], 1925, 0, 0],
    ]
    return pd.DataFrame(data=d, columns=cols)

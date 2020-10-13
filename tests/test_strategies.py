from optopsy.strategies import *
from optopsy.definitions import *


describe_cols = [
    "count",
    "mean",
    "std",
    "min",
    "25%",
    "50%",
    "75%",
    "max",
]


def test_single_long_calls_raw(data):
    results = long_calls(data, raw=True)
    assert len(results) == 4
    assert list(results.columns) == single_strike_internal_cols
    assert round(results.iloc[0]["pct_change"], 2) == 2.31
    assert round(results.iloc[1]["pct_change"], 2) == 2.42
    assert round(results.iloc[2]["pct_change"], 2) == 2.53
    assert round(results.iloc[3]["pct_change"], 2) == 2.66


def test_single_long_puts_raw(data):
    results = long_puts(data, raw=True)
    assert len(results) == 4
    assert list(results.columns) == single_strike_internal_cols
    assert round(results.iloc[0]["pct_change"], 2) == -1
    assert round(results.iloc[1]["pct_change"], 2) == -1
    assert round(results.iloc[2]["pct_change"], 2) == -1
    assert round(results.iloc[3]["pct_change"], 2) == -1


def test_single_short_calls_raw(data):
    results = short_calls(data, raw=True)
    assert len(results) == 4
    assert list(results.columns) == single_strike_internal_cols

    # shorting naked calls can have infinite losses
    assert round(results.iloc[0]["pct_change"], 2) == -2.31
    assert round(results.iloc[1]["pct_change"], 2) == -2.42
    assert round(results.iloc[2]["pct_change"], 2) == -2.53
    assert round(results.iloc[3]["pct_change"], 2) == -2.66


def test_single_short_puts_raw(data):
    results = short_puts(data, raw=True)
    assert len(results) == 4
    assert list(results.columns) == single_strike_internal_cols
    assert round(results.iloc[0]["pct_change"], 2) == 1
    assert round(results.iloc[1]["pct_change"], 2) == 1
    assert round(results.iloc[2]["pct_change"], 2) == 1
    assert round(results.iloc[3]["pct_change"], 2) == 1


def test_singles_long_calls(data):
    results = long_calls(data)
    assert len(results) == 1
    assert results.iloc[0]["count"] == 4.0
    assert round(results.iloc[0]["mean"], 2) == 2.48
    assert list(results.columns) == single_strike_external_cols + describe_cols


def test_singles_long_puts(data):
    results = long_puts(data)
    assert len(results) == 1
    assert results.iloc[0]["count"] == 4.0
    assert round(results.iloc[0]["mean"], 2) == -1.0
    assert list(results.columns) == single_strike_external_cols + describe_cols


def test_singles_short_calls(data):
    results = short_calls(data)
    assert len(results) == 1
    assert results.iloc[0]["count"] == 4.0
    assert round(results.iloc[0]["mean"], 2) == -2.48
    assert list(results.columns) == single_strike_external_cols + describe_cols


def test_singles_short_puts(data):
    results = short_puts(data)
    assert len(results) == 1
    assert results.iloc[0]["count"] == 4.0
    assert round(results.iloc[0]["mean"], 2) == 1.0
    assert list(results.columns) == single_strike_external_cols + describe_cols


def test_straddles_long_raw(data):
    results = long_straddles(data, raw=True)
    assert len(results) == 4
    assert list(results.columns) == single_strike_internal_cols
    assert round(results.iloc[0]["pct_change"], 2) == 0.86
    assert round(results.iloc[1]["pct_change"], 2) == 0.83
    assert round(results.iloc[2]["pct_change"], 2) == 0.79
    assert round(results.iloc[3]["pct_change"], 2) == 0.75


def test_straddles_short_raw(data):
    results = short_straddles(data, raw=True)
    assert len(results) == 4
    assert list(results.columns) == single_strike_internal_cols
    assert round(results.iloc[0]["pct_change"], 2) == -0.86
    assert round(results.iloc[1]["pct_change"], 2) == -0.83
    assert round(results.iloc[2]["pct_change"], 2) == -0.79
    assert round(results.iloc[3]["pct_change"], 2) == -0.75


def test_long_straddles(data):
    results = long_straddles(data)
    assert len(results) == 1
    assert results.iloc[0]["count"] == 4.0
    assert round(results.iloc[0]["mean"], 2) == 0.81
    assert list(results.columns) == single_strike_external_cols + describe_cols


def test_short_straddles(data):
    results = short_straddles(data)
    assert len(results) == 1
    assert results.iloc[0]["count"] == 4.0
    assert round(results.iloc[0]["mean"], 2) == -0.81
    assert list(results.columns) == single_strike_external_cols + describe_cols


def test_strangles_long_raw(data):
    results = long_strangles(data, raw=True)
    assert len(results) == 6
    assert list(results.columns) == double_strike_internal_cols
    assert round(results.iloc[0]["pct_change"], 2) == 0.87
    assert round(results.iloc[1]["pct_change"], 2) == 0.88
    assert round(results.iloc[2]["pct_change"], 2) == 0.88
    assert round(results.iloc[3]["pct_change"], 2) == 0.84
    assert round(results.iloc[4]["pct_change"], 2) == 0.84
    assert round(results.iloc[5]["pct_change"], 2) == 0.79


def test_strangles_short_raw(data):
    results = short_strangles(data, raw=True)
    assert len(results) == 6
    assert list(results.columns) == double_strike_internal_cols
    assert round(results.iloc[0]["pct_change"], 2) == -0.87
    assert round(results.iloc[1]["pct_change"], 2) == -0.88
    assert round(results.iloc[2]["pct_change"], 2) == -0.88
    assert round(results.iloc[3]["pct_change"], 2) == -0.84
    assert round(results.iloc[4]["pct_change"], 2) == -0.84
    assert round(results.iloc[5]["pct_change"], 2) == -0.79


def test_long_strangles(data):
    results = long_strangles(data)
    assert len(results) == 1
    assert results.iloc[0]["count"] == 6.0
    assert round(results.iloc[0]["mean"], 2) == 0.85
    assert list(results.columns) == double_strike_external_cols + describe_cols


def test_short_strangles(data):
    results = short_strangles(data)
    assert len(results) == 1
    assert results.iloc[0]["count"] == 6.0
    assert round(results.iloc[0]["mean"], 2) == -0.85
    assert list(results.columns) == double_strike_external_cols + describe_cols


def test_long_call_spread_raw(data):
    results = long_call_spread(data, raw=True)
    assert len(results) == 6
    assert list(results.columns) == double_strike_internal_cols
    assert round(results.iloc[0]["pct_change"], 2) == 0.59
    assert round(results.iloc[1]["pct_change"], 2) == 0.64
    assert round(results.iloc[2]["pct_change"], 2) == 0.67
    assert round(results.iloc[3]["pct_change"], 2) == 0.69
    assert round(results.iloc[4]["pct_change"], 2) == 0.71
    assert round(results.iloc[5]["pct_change"], 2) == 0.72


def test_long_put_spread_raw(data):
    results = long_put_spread(data, raw=True)
    assert len(results) == 6
    assert list(results.columns) == double_strike_internal_cols
    assert round(results.iloc[0]["pct_change"], 2) == -1
    assert round(results.iloc[1]["pct_change"], 2) == -1
    assert round(results.iloc[2]["pct_change"], 2) == -1
    assert round(results.iloc[3]["pct_change"], 2) == -1
    assert round(results.iloc[4]["pct_change"], 2) == -1
    assert round(results.iloc[5]["pct_change"], 2) == -1


def test_short_call_spread_raw(data):
    results = short_call_spread(data, raw=True)
    assert len(results) == 6
    assert list(results.columns) == double_strike_internal_cols
    assert round(results.iloc[0]["pct_change"], 2) == -0.59
    assert round(results.iloc[1]["pct_change"], 2) == -0.64
    assert round(results.iloc[2]["pct_change"], 2) == -0.67
    assert round(results.iloc[3]["pct_change"], 2) == -0.69
    assert round(results.iloc[4]["pct_change"], 2) == -0.71
    assert round(results.iloc[5]["pct_change"], 2) == -0.72


def test_short_put_spread_raw(data):
    results = short_put_spread(data, raw=True)
    assert len(results) == 6
    assert list(results.columns) == double_strike_internal_cols
    assert round(results.iloc[0]["pct_change"], 2) == 1
    assert round(results.iloc[1]["pct_change"], 2) == 1
    assert round(results.iloc[2]["pct_change"], 2) == 1
    assert round(results.iloc[3]["pct_change"], 2) == 1
    assert round(results.iloc[4]["pct_change"], 2) == 1
    assert round(results.iloc[5]["pct_change"], 2) == 1


def test_long_call_butterfly_raw(data):
    results = long_call_butterfly(data, raw=True)
    assert len(results) == 4
    assert list(results.columns) == triple_strike_internal_cols
    assert round(results.iloc[0]["pct_change"], 2) == -1
    assert round(results.iloc[1]["pct_change"], 2) == -0.85
    assert round(results.iloc[2]["pct_change"], 2) == 0.56
    assert round(results.iloc[3]["pct_change"], 2) == -1

import pandas as pd
from .core import (
    _calls,
    _puts,
    _process_strategy,
    _format_output,
    _calculate_total_entry_exits,
    _calculate_pct_change,
)
from .definitions import (
    single_strike_external_cols,
    single_strike_internal_cols,
    double_strike_external_cols,
    double_strike_internal_cols,
    triple_strike_external_cols,
    triple_strike_internal_cols,
)
from .rules import _rule_non_overlapping_strike


default_kwargs = {
    "dte_interval": 7,
    "max_entry_dte": 90,
    "exit_dte": 0,
    "otm_pct_interval": 0.05,
    "max_otm_pct": 0.5,
    "min_bid_ask": 0.05,
    "drop_nan": True,
    "raw": False,
}


def _singles(data, leg_def, **kwargs):
    params = {**default_kwargs, **kwargs}
    return _process_strategy(
        data,
        internal_cols=single_strike_internal_cols,
        external_cols=single_strike_external_cols,
        leg_def=leg_def,
        params=params,
    )


def _straddles(data, leg_def, **kwargs):
    params = {**default_kwargs, **kwargs}

    return _process_strategy(
        data,
        internal_cols=single_strike_internal_cols,
        external_cols=single_strike_external_cols,
        leg_def=leg_def,
        join_on=[
            "underlying_symbol",
            "expiration",
            "strike",
            "dte_entry",
            "dte_range",
            "otm_pct_range",
            "underlying_price_entry",
        ],
        params=params,
    )


def _strangles(data, leg_def, **kwargs):
    params = {**default_kwargs, **kwargs}
    return _process_strategy(
        data,
        internal_cols=double_strike_internal_cols,
        external_cols=double_strike_external_cols,
        leg_def=leg_def,
        rules=_rule_non_overlapping_strike,
        join_on=["underlying_symbol", "expiration", "dte_entry", "dte_range"],
        params=params,
    )


def _vertical_spread(data, leg_def, **kwargs):
    params = {**default_kwargs, **kwargs}
    return _process_strategy(
        data,
        internal_cols=double_strike_internal_cols,
        external_cols=double_strike_external_cols,
        leg_def=leg_def,
        rules=_rule_non_overlapping_strike,
        join_on=["underlying_symbol", "expiration", "dte_entry", "dte_range"],
        params=params,
    )


def _butterflies(data, side, **kwargs):
    params = {**default_kwargs, **kwargs}

    # butterflies are basically one long call spread and one short call spread
    # where leg 2 of long call spread has same strike as leg 1 of short call spread
    if side == "call":
        long_spreads = long_call_spread(data, raw=True)
        short_spreads = short_call_spread(data, raw=True)
    else:
        long_spreads = long_put_spread(data, raw=True)
        short_spreads = short_put_spread(data, raw=True)

    # rename strike_leg2 of long_call_spreads to be used as key
    long_spreads.rename(columns={"strike_leg2": "strike_leg"}, inplace=True)
    short_spreads.rename(columns={"strike_leg1": "strike_leg"}, inplace=True)

    on = ["underlying_symbol", "expiration", "dte_entry", "strike_leg"]

    butterflies = pd.merge(long_spreads, short_spreads, on=on, how="inner")

    entry_cols = ["total_entry_cost_x", "total_entry_cost_y"]
    exit_cols = ["total_exit_proceeds_x", "total_exit_proceeds_y"]

    rename_cols = {
        "underlying_price_entry_leg1_x": "underlying_price_entry",
        "underlying_price_exit_leg1_x": "underlying_price_exit",
        "otm_pct_range_leg1_x": "otm_pct_range_leg1",
        "otm_pct_range_leg2_y": "otm_pct_range_leg3",
        "otm_pct_range_leg2_x": "otm_pct_range_leg2",
        "dte_range_x": "dte_range",
        "strike_leg2": "strike_leg3",
        "strike_leg": "strike_leg2",
    }

    return (
        butterflies.rename(columns=rename_cols)
        .pipe(_calculate_total_entry_exits, entry_cols, exit_cols)
        .pipe(_calculate_pct_change)
        .pipe(
            _format_output,
            params,
            triple_strike_internal_cols,
            triple_strike_external_cols,
        )
    )


def long_calls(data, **kwargs):
    return _singles(data, [(1, _calls)], **kwargs)


def long_puts(data, **kwargs):
    return _singles(data, [(1, _puts)], **kwargs)


def short_calls(data, **kwargs):
    return _singles(data, [(-1, _calls)], **kwargs)


def short_puts(data, **kwargs):
    return _singles(data, [(-1, _puts)], **kwargs)


def long_straddles(data, **kwargs):
    return _straddles(data, [(1, _puts), (1, _calls)], **kwargs)


def short_straddles(data, **kwargs):
    return _straddles(data, [(-1, _puts), (-1, _calls)], **kwargs)


def long_strangles(data, **kwargs):
    return _strangles(data, [(1, _puts), (1, _calls)], **kwargs)


def short_strangles(data, **kwargs):
    return _strangles(data, [(-1, _puts), (-1, _calls)], **kwargs)


def long_call_spread(data, **kwargs):
    return _vertical_spread(data, [(1, _calls), (-1, _calls)], **kwargs)


def short_call_spread(data, **kwargs):
    return _vertical_spread(data, [(-1, _calls), (1, _calls)], **kwargs)


def long_put_spread(data, **kwargs):
    return _vertical_spread(data, [(-1, _puts), (1, _puts)], **kwargs)


def short_put_spread(data, **kwargs):
    return _vertical_spread(data, [(1, _puts), (-1, _puts)], **kwargs)


def long_call_butterfly(data, **kwargs):
    return _butterflies(data, "call", **kwargs)

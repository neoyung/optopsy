from .core import _calls, _puts, _process_strategy
from .definitions import (
    single_strike_external_cols,
    single_strike_internal_cols,
    double_strike_external_cols,
    double_strike_internal_cols,
    straddle_internal_cols,
)
from .rules import _rule_non_overlapping_strike
from enum import Enum
from .verbose import VERBOSE

default_kwargs = {
    "dte_interval": 7,  # time difference in terms of expiry dates of option chain for result output dataframe
    "max_entry_dte": 90,  # max time2expiry in days
    "exit_dte": 0,  # 0 means hold to maturity, 2 means exit 2 days prior to expiry
    "otm_pct_interval": 0.025,
    "max_otm_pct": 0.2,  # HARD_LIMIT: max out of the money percentage, 0.5 OTM = 50% OTM
    "min_bid_ask": 0.05,  # meaningless trade with no mkt, options with no bid-ask data will be pruned
    "volume": 0,  # remove illiquid options
    "drop_nan": True,  # drop NAN in final grpby operation
    "raw": False,  # final return df's columns, if raw, no data aggregation with basis stats
}


class Side(Enum):
    long = 1
    short = -1


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
        internal_cols=straddle_internal_cols,
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


def _call_spread(data, leg_def, **kwargs):
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


def _put_spread(data, leg_def, **kwargs):
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


def long_calls(data, **kwargs):
    return _singles(data, [(Side.long, _calls)], **kwargs)


def long_puts(data, **kwargs):
    return _singles(data, [(Side.long, _puts)], **kwargs)


def short_calls(data, **kwargs):
    return _singles(data, [(Side.short, _calls)], **kwargs)


def short_puts(data, **kwargs):
    return _singles(data, [(Side.short, _puts)], **kwargs)


def long_straddles(data, **kwargs):
    return _straddles(data, [(Side.long, _puts), (Side.long, _calls)], **kwargs)


def short_straddles(data, **kwargs):
    return _straddles(data, [(Side.short, _puts), (Side.short, _calls)], **kwargs)


def long_strangles(data, **kwargs):
    return _strangles(data, [(Side.long, _puts), (Side.long, _calls)], **kwargs)


def short_strangles(data, **kwargs):
    return _strangles(data, [(Side.short, _puts), (Side.short, _calls)], **kwargs)


def long_call_spread(data, **kwargs):
    return _call_spread(data, [(Side.long, _calls), (Side.short, _calls)], **kwargs)


def short_call_spread(data, **kwargs):
    return _call_spread(data, [(Side.short, _calls), (Side.long, _calls)], **kwargs)


def long_put_spread(data, **kwargs):
    return _put_spread(data, [(Side.short, _puts), (Side.long, _puts)], **kwargs)


def short_put_spread(data, **kwargs):
    return _put_spread(data, [(Side.long, _puts), (Side.short, _puts)], **kwargs)


all_strats = (
    long_calls,
    long_puts,
    short_calls,
    short_puts,
    long_straddles,
    short_straddles,
    long_strangles,
    short_strangles,
    long_call_spread,
    short_call_spread,
    long_put_spread,
    short_put_spread,
)

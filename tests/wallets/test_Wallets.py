from itertools import chain

from visfin.configs.columns import WALLET_COLUMN
from visfin.configs.wallets import (
    ASN_WALLET,
    DUO_DEBT_WALLET,
    WALLET_MAPPING,
    WBW_SISTER,
)
from visfin.wallets import Wallets


def test_initialization(sample_data):
    wallets_obj = Wallets(sample_data)
    assert wallets_obj is not None
    assert hasattr(wallets_obj, "df")
    assert hasattr(wallets_obj, "date_column")
    # Add more assertions to check other attributes


def test_filter_wallets(sample_data):
    wallets_obj = Wallets(sample_data)
    filtered_df = wallets_obj.filter_wallets([DUO_DEBT_WALLET, ASN_WALLET])
    assert filtered_df[WALLET_COLUMN].nunique() == 2


def test_get_balance_over_time(sample_data):
    wallets_obj = Wallets(sample_data)
    balance_df = wallets_obj.get_balance_over_time()
    assert len(balance_df) > 0
    # Add more assertions to check the generated DataFrame


def test_combine_wallets(sample_data):
    wallets_obj = Wallets(sample_data)
    combined_df = wallets_obj.combine_wallets(WALLET_MAPPING)
    assert combined_df[WALLET_COLUMN].nunique() == sample_data[
        WALLET_COLUMN
    ].nunique() - len(set(chain(*WALLET_MAPPING.values())))
    # Add more assertions to check the combined wallet values


def test_get_wallet_subgroup(sample_data):
    wallets_obj = Wallets(sample_data)
    subgroup = wallets_obj.get_wallet_subgroup([DUO_DEBT_WALLET, WBW_SISTER])
    assert subgroup is not None
    assert hasattr(subgroup, "df")
    assert hasattr(subgroup, "wallets")
    # Add more assertions to check other attributes


# Add more test cases as needed

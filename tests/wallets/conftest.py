import pandas as pd
import pytest

from visfin.configs.columns import (
    AMOUNT_COLUMN,
    CATEGORY_COLUMN,
    DATE_COLUMN,
    LABEL_COLUMN,
    TYPE_COLUMN,
    WALLET_COLUMN,
)
from visfin.configs.wallets import (
    ASN_WALLET,
    CASH_WALLET,
    CRYPTO_WALLET,
    DEBIT_WALLET,
    DUO_DEBT_WALLET,
    DUO_INVEST_WALLET,
    EXPECTED_TAXES_WALLET,
    FIXED_CHARGES_WALLET,
    ING_WALLET,
    INVEST_WALLET,
    KOOPZEGEL_WALLET,
    REVOLUT_WALLET,
    SAVINGS_WALLET,
    SPLIT_WALLET,
    WBW_DISPUUT,
    WBW_FRIENDS,
    WBW_SISTER,
)


# Sample data for testing
@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            DATE_COLUMN: [
                "2023-01-01",
                "2023-01-01",
                "2023-01-01",
                "2023-01-01",
                "2023-01-01",
                "2023-01-02",
                "2023-01-02",
                "2023-01-02",
                "2023-01-02",
                "2023-01-02",
                "2023-01-03",
                "2023-01-03",
                "2023-01-03",
                "2023-01-03",
                "2023-01-03",
                "2023-01-04",
                "2023-01-04",
                "2023-01-04",
                "2023-01-04",
                "2023-01-04",
                "2023-01-05",
                "2023-01-05",
                "2023-01-05",
                "2023-01-05",
                "2023-01-05",
            ],
            LABEL_COLUMN: [
                "LabelA",
                "LabelB",
                "LabelC",
                "LabelD",
                "LabelE",
                "LabelF",
                "LabelG",
                "LabelH",
                "LabelI",
                "LabelJ",
                "LabelK",
                "LabelL",
                "LabelM",
                "LabelN",
                "LabelO",
                "LabelP",
                "LabelQ",
                "LabelR",
                "LabelS",
                "LabelT",
                "LabelU",
                "LabelV",
                "LabelW",
                "LabelX",
                "LabelY",
            ],
            TYPE_COLUMN: [
                "Incoming Transfer",
                "Outgoing Transfer",
                "Expense",
                "Income",
                "Incoming Transfer",
                "Outgoing Transfer",
                "Expense",
                "Income",
                "Incoming Transfer",
                "Outgoing Transfer",
                "Expense",
                "Income",
                "Incoming Transfer",
                "Outgoing Transfer",
                "Expense",
                "Income",
                "Incoming Transfer",
                "Outgoing Transfer",
                "Expense",
                "Income",
                "Incoming Transfer",
                "Outgoing Transfer",
                "Expense",
                "Income",
                "Incoming Transfer",
            ],
            AMOUNT_COLUMN: [
                100,
                -50,
                75,
                -30,
                200,
                -10,
                30,
                -25,
                -50,
                100,
                75,
                -20,
                150,
                -60,
                40,
                20,
                -80,
                10,
                5,
                -15,
                120,
                -70,
                50,
                60,
                -45,
            ],
            WALLET_COLUMN: [
                DUO_DEBT_WALLET,
                WBW_SISTER,
                WBW_FRIENDS,
                WBW_DISPUUT,
                CASH_WALLET,
                ING_WALLET,
                KOOPZEGEL_WALLET,
                REVOLUT_WALLET,
                ASN_WALLET,
                FIXED_CHARGES_WALLET,
                EXPECTED_TAXES_WALLET,
                DEBIT_WALLET,
                DUO_INVEST_WALLET,
                SPLIT_WALLET,
                INVEST_WALLET,
                CRYPTO_WALLET,
                SAVINGS_WALLET,
                DUO_DEBT_WALLET,
                WBW_SISTER,
                WBW_FRIENDS,
                DUO_DEBT_WALLET,
                WBW_SISTER,
                INVEST_WALLET,
                CRYPTO_WALLET,
                SAVINGS_WALLET,
            ],
            CATEGORY_COLUMN: [
                "CategoryA",
                "CategoryB",
                "CategoryA",
                "CategoryC",
                "CategoryB",
                "CategoryA",
                "CategoryC",
                "CategoryB",
                "CategoryD",
                "CategoryA",
                "CategoryC",
                "CategoryB",
                "CategoryA",
                "CategoryD",
                "CategoryB",
                "CategoryC",
                "CategoryB",
                "CategoryA",
                "CategoryD",
                "CategoryB",
                "CategoryA",
                "CategoryD",
                "CategoryA",
                "CategoryB",
                "CategoryD",
            ],
        }
    ).assign(
        **{DATE_COLUMN: lambda df: pd.to_datetime(df[DATE_COLUMN], format="%Y-%m-%d")}
    )

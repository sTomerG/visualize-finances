import itertools
from typing import Literal, Optional

import pandas as pd
from loguru import logger

from visfin.configs.columns import (
    ALL_COLUMNS,
    AMOUNT_COLUMN,
    BALANCE_COLUMN,
    DATE_COLUMN,
    WALLET_COLUMN,
)
from visfin.configs.wallets import ALL_WALLETS, INITIAL_BALANCES, WALLET_MAPPING


class Wallets:
    """
    A class representing a collection of wallets and their transactions.
    """

    def __init__(
        self,
        df: pd.DataFrame,
        date_column: str = DATE_COLUMN,
        amount_column: str = AMOUNT_COLUMN,
        wallet_column: str = WALLET_COLUMN,
        all_columns: list[str] = ALL_COLUMNS,
        wallet_mapping: dict[str, list[str]] = WALLET_MAPPING,
        initial_balances: dict[str, float] = INITIAL_BALANCES,
        all_wallets: set[str] = ALL_WALLETS,
    ) -> None:
        """
        Initialize the Wallets object.

        Parameters:
            df (pd.DataFrame): The raw data containing transactions.
            date_column (str): Column name for date values.
            amount_column (str): Column name for transaction amount values.
            wallet_column (str): Column name for wallet identifiers.
            all_columns (list[str]): List of all columns in the raw data.
            wallet_mapping (dict[str, list[str]]): Mapping of old wallet identifiers to new ones.
            initial_balances (dict[str, float]): Initial balances for each wallet.
            all_wallets (set[str]): Set of all wallet identifiers.
        """
        self.df_raw = df
        self.date_column = date_column
        self.amount_column = amount_column
        self.wallet_column = wallet_column
        self.all_columns = all_columns
        self.wallet_mapping = wallet_mapping
        self.initial_balances = initial_balances
        self.all_wallets = all_wallets
        self._test_data()
        self.df = self._process_df()

    def _test_data(self):
        """
        Test if the wallet identifiers in the data match the configured set of wallet identifiers.
        """
        logger.debug("Testing the data")
        different_wallets = self.all_wallets ^ set(
            self.df_raw[self.wallet_column].unique().tolist()
        )
        if len(different_wallets) > 0:
            logger.warning(
                f"Difference in wallets between config and data: {different_wallets}"
            )
        different_columns = self.all_columns - set(self.df_raw.columns)
        if len(different_columns) > 0:
            logger.error(
                f"Columns found in config but not in data: {different_columns}"
            )

    def filter_wallets(
        self, wallets: list[str], df: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        """
        Filter transactions based on a list of wallet identifiers.

        Parameters:
            wallets (list[str]): List of wallet identifiers to be filtered.
            df (Optional[pd.DataFrame]): DataFrame to be filtered. If not provided, the object's DataFrame is used.

        Returns:
            pd.DataFrame: Filtered DataFrame containing transactions only for the specified wallets.
        """
        df = df if df is not None else self.df
        return df.loc[lambda df: df[self.wallet_column].isin(wallets)]

    def _process_df(
        self,
    ) -> pd.DataFrame:
        """
        Process the raw data to create a DataFrame with additional columns and calculated values.

        Returns:
            pd.DataFrame: Processed DataFrame.
        """
        logger.info(f"Total amount of transactions = {len(self.df_raw)}")
        logger.info(
            f"Data spans from {self.df_raw[self.date_column].min()} until {self.df_raw[self.date_column].max()} "
        )
        return (
            self.df_raw.loc[:, list(self.all_columns)]
            .pipe(lambda df: self._add_initial_balance(df=df))
            .pipe(lambda df: self.combine_wallets(df=df, mapping=self.wallet_mapping))
        )

    def _add_initial_balance(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add initial balance rows to the DataFrame.

        Parameters:
            df (pd.DataFrame): DataFrame to which initial balance rows will be added.

        Returns:
            pd.DataFrame: DataFrame with initial balance rows.
        """
        logger.debug("Adding initial balances")
        wallets = df[self.wallet_column].unique()

        min_date = df[self.date_column].min() - pd.Timedelta(
            days=1
        )  # One day before the first date

        df_dict = {
            self.wallet_column: wallets,
            self.amount_column: [
                self.initial_balances[wallet.strip()] for wallet in wallets
            ],
            self.date_column: [min_date] * len(wallets),
        }
        df_init = pd.DataFrame(df_dict, index=list(range(-len(wallets), 0)))
        return pd.concat([df_init, df])

    def get_balance_over_time(self, freq: Literal["H", "D"] = "D") -> pd.DataFrame:
        """
        Calculate wallet balances over time.

        Parameters:
            freq (Literal["H", "D"]): Frequency for time intervals ("H" for hours, "D" for days).

        Returns:
            pd.DataFrame: DataFrame containing wallet balances over time.
        """
        logger.debug("Retrieving balance over time")
        df = self.df.copy()

        df[self.date_column] = pd.to_datetime(df[self.date_column])
        df.set_index(self.date_column, inplace=True)

        df = pd.concat([df, df.assign(**{WALLET_COLUMN: "Total"})])
        # This will create a Series
        df_grouped = (
            df.groupby(self.wallet_column).resample(freq)[self.amount_column].sum()
        )

        # Convert Series to DataFrame
        df_grouped = df_grouped.reset_index().rename(columns={0: self.amount_column})

        min_date = df.index.min().floor(freq)
        max_date = df.index.max().floor(freq)

        all_wallets = df[self.wallet_column].unique()
        all_dates = pd.date_range(start=min_date, end=max_date, freq=freq)

        # Generate all combinations of dates and wallets
        df_all = pd.DataFrame.from_records(
            itertools.product(all_wallets, all_dates),
            columns=[self.wallet_column, self.date_column],
        )

        # Merge dataframes
        df_grouped = pd.merge(
            df_all,
            df_grouped,
            how="left",
            on=[self.wallet_column, self.date_column],
        ).fillna(0)

        return (df_grouped.sort_values(self.date_column)).assign(
            **{
                BALANCE_COLUMN: lambda df: df.groupby(self.wallet_column)[
                    self.amount_column
                ].cumsum()
            }
        )

    def combine_wallets(
        self,
        mapping: dict[str, str],
        df: Optional[pd.DataFrame] = None,
    ) -> pd.DataFrame:
        """
        Combine wallet identifiers according to the given mapping.

        Parameters:
            mapping (dict[str, str]): Mapping of old wallet identifiers to new ones.
            df (Optional[pd.DataFrame]): DataFrame to be processed. If not provided, the object's DataFrame is used.

        Returns:
            pd.DataFrame: DataFrame with combined wallet identifiers.
        """
        df = df if df is not None else self.df
        logger.debug(f"Combining wallets: {mapping}")
        reverse_mapping = {
            old_value: new_value
            for new_value, old_values in mapping.items()
            for old_value in old_values
        }
        return df.assign(
            **{self.wallet_column: df[self.wallet_column].replace(reverse_mapping)}
        )

    def get_wallet_subgroup(self, wallets: list[str]):
        """
        Get a subgroup of wallets from the data.

        Parameters:
            wallets (list[str]): List of wallet identifiers for the subgroup.

        Returns:
            _WalletGroup: A _WalletGroup object containing the subgroup data.
        """
        logger.debug(f"Creating a WalletGroup with wallets: {wallets}")
        return _WalletGroup(self.df, wallets)


class _WalletGroup(Wallets):
    def __init__(self, df: pd.DataFrame, wallets: list[str]) -> None:
        super().__init__(df)
        del self.df_raw
        self.df = self.filter_wallets(wallets=wallets, df=df)
        self.wallets = wallets

    def _test_data(self):
        pass

    def _process_df(self) -> None:
        return None

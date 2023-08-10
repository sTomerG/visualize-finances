import glob
import os

import pandas as pd
import streamlit as st
from loguru import logger

from visfin.configs.columns import CATEGORY_COLUMN, DATE_COLUMN, WALLET_COLUMN


@st.cache_data
def concatenate_csv_files(
    folder_path: str = "data",
    date_column: str = DATE_COLUMN,
    wallet_column: str = WALLET_COLUMN,
    category_column: str = CATEGORY_COLUMN,
):
    # Use glob to find all CSV files in the folder
    csv_files = glob.glob(os.path.join(folder_path, "*.csv"))
    logger.info(f"Found {len(csv_files)} csv files")

    # Check if there are any CSV files in the folder
    if not csv_files:
        raise Exception("No CSV files found in the folder.")
    # Read and concatenate all CSV files into a single dataframe
    concatenated_df = pd.concat(
        [pd.read_csv(file, parse_dates=[date_column]) for file in csv_files],
        ignore_index=True,
    )
    concatenated_df = concatenated_df.rename(columns={"Category name": category_column})
    if concatenated_df[wallet_column].nunique() != len(csv_files):
        logger.warning(
            "Missing "
            f"{len(csv_files) - concatenated_df[wallet_column].nunique()} "
            "wallets!"
        )
    return concatenated_df

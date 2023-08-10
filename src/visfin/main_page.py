import plotly.express as px
import streamlit as st

from visfin.configs.columns import BALANCE_COLUMN, DATE_COLUMN, WALLET_COLUMN
from visfin.main import wallets

st.set_page_config(layout="wide")


df_balance = wallets.get_balance_over_time()

# Create the line chart using Plotly Express
fig = px.line(
    df_balance,
    x=DATE_COLUMN,
    y=BALANCE_COLUMN,
    color=WALLET_COLUMN,
    title="Balance Over Time",
)

# Show the plot
st.plotly_chart(fig, use_container_width=True)

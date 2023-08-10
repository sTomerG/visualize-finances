from visfin.utils import concatenate_csv_files
from visfin.wallets import Wallets

df_raw = concatenate_csv_files()
wallets = Wallets(df_raw)

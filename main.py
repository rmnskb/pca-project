# TODO: create a script which will update the DB once per business day after market closure
from pca_dax import data_handler as dh

data = dh.DataHandler(
    start_date='2010-01-01'
)

df = data.create_mean_var_df()

print(df.head())


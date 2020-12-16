"""
Script to populate database with currency and sales data.
"""

from ccy_data import *
from sales_data import *


def add_table(conn, table_data: pd.DataFrame, table_name):
    table_data.to_sql(table_name, conn, if_exists='replace')


usd_daily_ex_rates_df = get_complete_usd_daily_ex_rates(DATA_DATE_RANGE_START, DATA_DATE_RANGE_END)
usd_daily_ex_rates_df.sort_values('effectiveDate', inplace=True)
orders_value_daily_data = get_orders_value_daily(DATA_DATE_RANGE_START, DATA_DATE_RANGE_END)

db_conn = get_db_connection(PATH_TO_DB)
add_table(db_conn, usd_daily_ex_rates_df, USD_EX_RATES_TABLE_NAME)
add_table(db_conn, orders_value_daily_data, SALES_TABLE_NAME)

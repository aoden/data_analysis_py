__author__ = 'aoden'
import pandas as pd
from pandas import DataFrame
import datetime


sp500 = pd.io.data.get_data_yahoo('%5EGSPC',
                                  start=datetime.datetime(2000, 10, 1),
                                  end=datetime.datetime(2012, 1, 1))

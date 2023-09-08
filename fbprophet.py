# This will open a new tab in your default web browser and display the Plotly graph

from datetime import datetime, timedelta

import pandas as pd
import plotly.io as pio
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly

symbol = input("Enter stock symbol e.g. AAPL, or GEAR.AX for aussie stocks: ")

# Get the current date and calculate the start date for the last 3 years
end_date = datetime.now()
start_date = end_date - timedelta(days=1095)

# Get the data for the stock
data = yf.download(symbol, start_date, end_date)
data.sort_values(by=["Date"], inplace=True)

# dump data to csv
data.to_csv("data.csv")

# copy the yahoo dataframe for modification
df = data.copy()

# reset the index of the df dataframe
df.reset_index(inplace=True)

# select just the date and the price
df = df[["Date", "Close"]]

# rename the features
df = df.rename(columns={"Date": "ds", "Close": "y"})

fbp = Prophet(daily_seasonality=True)
fbp.fit(df)
future = fbp.make_future_dataframe(periods=365)
forecast = fbp.predict(future)

# set the default plot renderer to 'browser'
pio.renderers.default = "browser"

# display the figure using plotly.io.show()
fig = plot_plotly(fbp, forecast)
pio.show(fig)

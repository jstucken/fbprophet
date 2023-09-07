# This will open a new tab in your default web browser and display the Plotly graph

from prophet import Prophet
import yfinance as yf
import pandas as pd
import plotly.io as pio
from datetime import datetime, timedelta

symbol = input("Enter stock symbol e.g. AAPL, or GEAR.AX for aussie stocks: ")

# Get the current date and calculate the start date for the last 3 years
end_date = datetime.now()
start_date = end_date - timedelta(days=1095)

# Get the data for the stock
data = yf.download(symbol, start_date, end_date)
data.sort_values(by=["Date"], inplace=True)

# save a csv
data.to_csv("data.csv")

df = pd.read_csv("data.csv")

# select the date and the price
df = df[["Date", "Close"]]

# rename the features
df = df.rename(columns={"Date": "ds", "Close": "y"})

fbp = Prophet(daily_seasonality=True)
fbp.fit(df)
future = fbp.make_future_dataframe(periods=365)
forecast = fbp.predict(future)

# import the facebooks prophet plotting libraries
from prophet.plot import plot_plotly

# set the default renderer to 'browser'
pio.renderers.default = "browser"

# display the figure using plotly.io.show()
fig = plot_plotly(fbp, forecast)
pio.show(fig)

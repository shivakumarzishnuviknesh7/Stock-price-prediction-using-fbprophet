# -*- coding: utf-8 -*-
"""FINAL YEAR PROJECT .ipynb

Original file is located at
    https://colab.research.google.com/drive/1lPidGTsD5_-4MkK5oAQbQ6Z332YHIj4n
"""

!pip install streamlit

!pip install yfinance

%%writefile final.py

import streamlit as st
from datetime import date
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go

START = "2015-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.title('Stock Price Prediction Application')

stocks = ('BAJAJFINSV.NS', 'TATAMOTORS.NS', 'BAJFINANCE.NS', 'JSWSTEEL.NS', 'COALINDIA.NS', 'ICICIBANK.NS', 'RELIANCE.NS', 'APOLLOHOSP.NS', 'ITC.NS', 'HDFCBANK.NS', 'TATASTEEL.NS', 'GRASIM.NS', 'AXISBANK.NS', 'KOTAKBANK.NS', 'SBIN.NS', 'HDFCBANK.NS', 'INDUSINDBK.NS', 'HCLTECH.NS', 'HINDALCO.NS', 'INFY.NS', 'M&M.NS', 'BAJAJ-AUTO.NS', 'TATAMOTORS.NS', 'TECHM.NS', 'NESTLEIND.NS', 'ONGC.NS', 'BHARTIARTL.NS', 'TCS.NS', 'HINDUNILVR.NS', 'BRITANNIA.NS', 'NTPC.NS', 'EICHERMOT.NS', 'TATACONSUM.NS', 'MARUTI.NS', 'ADANIPORTS.NS', 'HEROMOTOCO.NS', 'SBILIFE.NS', 'POWERGRID.NS', 'DIVISLAB.NS', 'ULTRACEMCO.NS', 'LT.NS', 'SUNPHARMA.NS', 'UPL.NS', 'CIPLA.NS', 'ASIANPAINT.NS', 'DRREDDY.NS', 'BPCL.NS', 'BPCL.NS', 'HDFCLIFE.NS', 'SHREECEM.NS', 'WIPRO.NS')
selected_stock = st.selectbox('Select company for prediction', stocks)

n_years = st.slider('Years of prediction:', 1, 10)
period = n_years * 365

@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data


data_load_state = st.text('Loading data...')
data = load_data(selected_stock)
data_load_state.text('Loading data... done!')

st.subheader('last five dates data')
st.write(data.tail())

# Plot raw data
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    fig.layout.update(title_text='Time Series data with Rangeslider', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()

#forecasting
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

st.subheader('Forecast data')
st.write(forecast.tail())

st.write('Stock Predicted Price')
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.write('forecast price trends')
fig2=m.plot_components(forecast)
st.write(fig2)



!streamlit run final.py & npx localtunnel --port 8501
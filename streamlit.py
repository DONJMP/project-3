import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Set page title
st.title('Stock Analysis App')

# Sidebar for user input
st.sidebar.header('User Input')
ticker = st.sidebar.text_input('Enter Stock Ticker', 'AAPL')

start_date= st.date_input("select start date", datetime.date.today()-datetime.timedelta(days=110))
end_date= st.date_input("select end date", datetime.date.today())
# Fetch stock data
@st.cache_data()
def load_data(ticker,start_date,end_date):
    stock_data = yf.download(ticker, start=start_date,end=end_date)
    return stock_data

stock_data = load_data(ticker,start_date,end_date)

# Daily returns
daily_returns = stock_data['Close'].pct_change()
             
sum_stat = daily_returns.describe()

def plot_candlestick(data, title):
    """
    This function plots a candlestick chart for the given data
    args:
        data: the dataframe containing historical crypto price
        title: the title of the plot
    """

    data['EMA_8'] = data['Close'].ewm(span=8, adjust=False).mean()
    data['EMA_21'] = data['Close'].ewm(span=21, adjust=False).mean()
    data['EMA_200'] = data['Close'].ewm(span=200, adjust=False).mean()


    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.10, subplot_titles=(f"{ticker} Candlestick Chart", 'Volume'),
                        row_width=[0.2, 0.7])
    # Volume
    fig.add_trace(go.Bar(x=data.index, y=data['Volume'], marker_color='lime', showlegend=False), row=2, col=1)

    # Candlestick chart
    fig.add_trace(go.Candlestick(x=data.index,
                                open=data["Open"],
                                high=data["High"],
                                low=data["Low"],
                                close=data["Close"],
                                increasing_line_color= 'green', 
                                decreasing_line_color= 'red',
                                name="OHLC"),
                row=1, col=1)
#Add EMAS
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA_8'], mode='lines', line=dict(color='blue'), name='EMA 8'), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA_21'], mode='lines', line=dict(color='orange'), name='EMA 21'), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data['EMA_200'], mode='lines', line=dict(color='purple'), name='EMA 200'), row=1, col=1)

    fig.update_layout(
        xaxis_tickfont_size=12,
        yaxis=dict(
            title='Price ($)',
            titlefont_size=18,
            tickfont_size=12,
            color = 'white'
        ),
        xaxis=dict(
            color = 'white'
        ),
        autosize=True,
        width=900,
        height=900,
        margin=dict(l=50, r=50, b=100, t=100, pad=4),
        paper_bgcolor='black',
        plot_bgcolor = 'black'
    )
    # Remove range slider; (short time frame)
    fig.update(layout_xaxis_rangeslider_visible=False)

    fig.show()
    return fig

col1, col2 = st.columns([1,3])
with col1:
    st.subheader('Stock Data Frames')

    display_option = st.radio("view stock data",
                            ( "stock data","daily returns","summary statistics"))
    if display_option == "stock data":
        st.write(stock_data)

    elif display_option == ("daily returns"):
        st.write(daily_returns)

    else: 
        st.write(sum_stat)

with col2:
    st.subheader("Visualizations")
    plot_options = st.radio(
        "select a visualization",
        ("line chart","candlestick chart")
    )
    if plot_options == "line chart":
        st.line_chart(stock_data['Close'])
    else: 
        st.plotly_chart(plot_candlestick(stock_data, 'Bitcoin 6 Month Candlestick Chart'))

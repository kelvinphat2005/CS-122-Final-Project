# Financial Market Analysis Dashboard

## Authors
- Kelvin Phat
- Jonah Wong

## Project Description
Our app is a Flask web application that collects publicly available historical stock-market data from the web. The purpose of our app is to provide an easy way for users to access historical stock data and to view in an easy to understand way. Our app will also be able to analyze the collected stock data. This analysis includes the analysis of price changes, daily returns, moving averages, and volatility for selected stocks. It will display the results using tables and visualizations such as price charts, volume charts, and return comparisons. 

## Project Outline/Plan

### Interface
Our application will be created using Python and Flask. There will be at least two pages. One for the home page and another one for an analysis page. We will utilize HTML components for user interactivity including, but not limited to:
- start date selector
- end date selector 
- input boxes
- refresh/collect data button
- frequency drop-down
- charts
- drop downs
- form buttons
- navigation buttons

There will be two main pages:

1. Home Page - Users will be able to visualize stock market data, with controls that allow users to customize a date-range. Users will also be able to view information about stock prices and trading volume. 

2. Analysis Page - Our app will also analyze stock information, like price changes, returns, and daily averages. All this information will be visualized with graphs, tables, and charts.

### Data Collection & Storage Plan
Our program will utilize Yahoo Finance free plan via the `yfinance` Python package to retrieve 5 years of financial data, and more. To avoid being rate limited, our program will cache data locally and retrieve on a user defined interval or manually refreshed.

For each selected stock, the program will collect data relating to:
- the date
- opening price
- highest price
- lowest price
- closing price
- trading volume

This data will be stored using `SQLite`, after the data has been cleaned.


### Data Analysis and Visualization Plan

Once stock data has been collected and stored, our tool will use **pandas** and **NumPy** to analyze it and **Matplotlib** (with **Plotly** for interactive charts) to visualize the results. The goal is to turn raw daily price data into clear metrics and charts that help a user understand how a stock has performed and how it compares to others.

#### Data Preparation
- Load stored price data (Date, Open, High, Low, Close, Adjusted Close, Volume) into a pandas DataFrame indexed by date.
- Clean the data by removing duplicate rows, handling missing values (e.g., market holidays) with forward-fill, and ensuring correct data types.
- Let the user filter the data by ticker symbol and date range (e.g., 1 month, 6 months, 1 year, 5 years).

#### Visualizations
1. **Price History Line Chart:** closing price over time, with optional 20/50/200-day moving average overlays.
2. **Candlestick Chart:** daily open, high, low, and close prices (interactive, using Plotly).
3. **Volume Bar Chart:** daily trading volume displayed beneath the price chart.
4. **Cumulative Return Comparison:** multiple stocks plotted on one chart to compare performance over the same period.
5. **Daily Returns Histogram:** the distribution of daily returns, showing how volatile a stock is.
6. **Correlation Heatmap:** a color-coded matrix showing how strongly selected stocks move together.
7. **RSI Chart:** RSI plotted over time with reference lines at 30 (oversold) and 70 (overbought).

#### Output to the User
- Key metrics will be displayed in a summary table alongside the charts in the interface.
- Users will be able to choose which stocks, time range, and indicators to display.
- Charts can be saved as PNG files, and analysis results can be exported to CSV.

#### Limitations
This tool analyzes **historical** data only and is intended for educational purposes. Past performance does not predict future results, and the tool does not provide investment advice.


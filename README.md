# Financial Market Analysis Dashboard

## Authors
- Kelvin Phat
- Jonah Wong

## Project Description
Our app is a Flask web application that collects publicly available historical stock-market data from the web. 

1. Home Page - Users will be able to visualize stock market data, with controls that allow users to customize a date-range. Users will also be able to view information about stock prices and trading volume. 

2. Analysis Page - Our app will also analyze stock information, like price changes, returns, and daily averages. All this information will be visualized with graphs, tables, and charts.

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


### Data Analysis & Visualization Plan
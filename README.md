# Stock_Project: Project Overview
- This project uses the Alpha Vantage API services to pull desired stock data on target symbols.
- Utilizes Quote Endpoint which is A lightweight alternative to the time series APIs, this service returns the price and volume information for a security of your choice.
- Utilizes Monthly Time Series which This API returns monthly adjusted time series (last trading day of each month, monthly open, monthly high, monthly low, monthly close, monthly adjusted close, monthly volume, monthly dividend) of the equity specified, covering 20+ years of historical data.
- Provides various data visualizations wth candlestick and line plots showing changes in OHLC information.
- Stock data and API functions are dependent on a txt file with target symbols and serves as main input for child operations in this project.

# Code & Resources 
#### Python Version: 3.7
#### Alpha Vantage API: https://www.alphavantage.co/documentation/
#### Packages: pandas, mplfinance, matplotlib, sqllite3, sqlalchemy

# Data Extraction:
### Quote Endpoint API: Attributes 
  - *SYMBOL|OPEN|HIGH|LOW|PRICE|VOLUME|LATEST TRADING DAY|PREVIOUS CLOSE|CHANGE|CHANGE%*
### Monthly Time Series API: Attributes 
  - *DATE|OPEN|HIGH|LOW|CLOSE|VOLUME*
### Alpha Vantage API Restrictions: *This project follows API requests per minute ad includes 60sec timer between API function invocation.*

# SQL Query/Dataframe Filtering Process: 
### Method 1: Dataframe
  * Filtered stock monthly data from 2019 - 2020 using boolean condition embeded into Dataframe.
  * This method is ideal based on simplicity and could reduce source code.
### Method 2: SQL
  * Filtered 2019-2020 stock data using query and inserting results into Dataframe.
  * This method is ideal for complex data filtering which a Dataframe can be limited to produce.
  * Provides fast temporary table creation in memory and could create sub tables from exccel sheets.

# Excel:Data Storage/Results
- **Stock_Global.xlsx** contains all stock data from Quote Endpount API request.
- **Stock_YTS.xlsx** contains all stock data from Monthly Time Series API request.
- **stocks.txt** contains target stock symbols.
- All data visualizations are saved automatically after every python execution.

# DATA VISUALIZATION #1: Candlestick Data
- Provides data visual on price movement on 4 different proces such as OHLC (open, high, low, close).
- A sub chart is also provided which plots monthly volume data from time from 2019 - 2020.
- This process is iterated which each stock symbol in stock.txt and dumps data visuals into desired direcory.
![](https://raw.githubusercontent.com/Adan-Macias/Stock_Project/master/Data_Visuals/candles/MSFT.png)
![](https://raw.githubusercontent.com/Adan-Macias/Stock_Project/master/Data_Visuals/candles/AMZN.png)

# DATA VISUALIZATION #2: Line Plot Data 
- This figure is composed of mutliple sub charts and plots OHLC data as per stock symbol.
- All charts share the X-axis and provides changes in prices for each symbol.
- Patterns and changes can be easily found on target stocks and provides easier comparisons between symbols, prices, and volumes.
![](https://raw.githubusercontent.com/Adan-Macias/Stock_Project/master/Data_Visuals/monthly_series/monthly_series.png)



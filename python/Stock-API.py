import urllib.request
import json
import pandas as pd
import numpy as np
import xlrd
import xlsxwriter
import time


# Request and retrieve response using API to access JSON data from aplhavantage website.
def QE_API(yourStock):
    stockURL = 'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol='+yourStock+'&apikey=V73E9ZM29Q7IN2I0'
    connection = urllib.request.urlopen(stockURL)
    responseString = connection.read().decode()
    return responseString

# Request and retrieve response using API to access JSON data from aplhavantage website.
def TS_Monthly_API(yourStock):
    stockURL = 'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol='+yourStock+'&apikey=V73E9ZM29Q7IN2I0'
    connection = urllib.request.urlopen(stockURL)
    responseString = connection.read().decode()
    return responseString

# Algorithm to split arrays/lists
def split_list(list, size):
    for i in range(0, len(list), size):
        yield list[i:i + size]

# This function calls TS_Monthly_API() as per stocks.txt symbols and pulls target data.
# Data is transferred to excel via Dataframe
def Time_Series_Monthly():
    # Data Arrays
    stockSymbol = []
    stockYears = []
    stockPrices = []

    # INPUT 
    file = open('C:/Users/melen/Desktop/PORTFOLIO/Stock_Project/stocks/stocks.txt', 'r')
    dataToExcel = pd.ExcelWriter("C:/Users/melen/Desktop/PORTFOLIO/Stock_Project/Data/Stock_YTS.xlsx", engine='xlsxwriter')

    # Algorithm for striping stock symbols from txt file and inserting into API functions.
    for stock in file:
        #Parse Stock Symbols
        stock = stock.strip()
        #API Stock URL
        responseString = TS_Monthly_API(stock)
        #JSON conversion to python
        data_out = json.loads(responseString)
      
        stockSymbol.append(data_out['Meta Data']['2. Symbol'])
        for year in data_out['Monthly Time Series']:
            stockYears.append(year)
        for year in data_out['Monthly Time Series'].values():
            stockPrices.append(year)

        # Dump stock data to sheets
        data = pd.DataFrame(stockPrices, index=stockYears)    
        data.index.names = ['DATE']
        data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        data.to_excel(dataToExcel, sheet_name=stockSymbol[0])

        # Reset Lists
        stockSymbol.clear()
        stockPrices.clear()
        stockYears.clear()
    dataToExcel.save()
    file.close()

# This function calls QE_API as per stocks.txt symbols and pulls target data.
# Data is transferred to excel via Dataframe.
def QEndpoint():
    # Data Arrays
    symbolList = []
    openList = []
    highList = []
    lowList = []
    priceList = []
    volumeList = []
    ltdList = []
    pcList = []
    changeList = []
    cpList = []

    # INPUT
    file = open('C:/Users/melen/Desktop/PORTFOLIO/Stock_Project/stocks/stocks.txt', 'r')
    for stock in file:
        #Parse Stock Symbols
        stock = stock.strip()
        #API Stock URL
        responseString = QE_API(stock)
        #JSON conversion to python
        data_out = json.loads(responseString)

        # Populate arrays for all stock symbols in stocks.txt
        # Echo parsed stock data for confirmation
        for x in data_out.values():
            stock_symbol = x['01. symbol']
            symbolList.append(stock_symbol)
            stock_open = float(x['02. open'])
            stock_high = float(x['03. high'])
            stock_low = float(x['04. low'])
            stock_price = float(x['05. price'])
            stock_volume = x['06. volume']
            stock_latest_trading_day = x['07. latest trading day']
            stock_previous_close = float(x['08. previous close'])
            stock_change = float(x['09. change'])
            stock_change_percentage = x['10. change percent']
        print('------------------ STOCK DATA FOR '+'['+stock_symbol+']'+' ---------------------\n')
        print('1.) Open ---> ', round(stock_open, 2))
        openList.append(round(stock_open, 2))
        print('2.) High ---> ', round(stock_high, 2))
        highList.append(round(stock_high, 2))
        print('3.) Low ---> ', round(stock_low, 2))
        lowList.append(round(stock_low, 2))
        print('4.) Price ---> ', round(stock_price, 2))
        priceList.append(round(stock_price, 2))
        print('5.) Volume ---> ', stock_volume)
        volumeList.append(stock_volume)
        print('6.) Latest Trading Day ---> ', stock_latest_trading_day)
        ltdList.append(stock_latest_trading_day)
        print('7.) Previous CLose ---> ', round(stock_previous_close, 2))
        pcList.append(round(stock_previous_close, 2))
        print('8.) Change ---> ', round(stock_change, 2))
        changeList.append(round(stock_change, 2))
        print('9.) Change Percent ---> ', stock_change_percentage)
        cpList.append(stock_change_percentage)

    # Send Stock Data to Excel sheet
    data = pd.DataFrame({'SYMBOL': symbolList,'OPEN': openList,'HIGH': highList,'LOW': lowList, 'PRICE': priceList,
        'VOLUME': volumeList, 'LATEST TRADING DAY': ltdList, 'PREVIOUS CLOSE': pcList, 
        'CHANGE': changeList, 'CHANGE %': cpList})        
    dataToExcel = pd.ExcelWriter("C:/Users/melen/Desktop/PORTFOLIO/Stock_Project/Data/Stock_Global.xlsx", engine='xlsxwriter')
    data.to_excel(dataToExcel, sheet_name='Stock-Global', index=False)
    dataToExcel.save()
    file.close()

def main():
    # Invoke Functions
    QEndpoint()

    print('\n.......60 sec Timer as per API limitations')
    #Following Alphavantage restrictions on data requests per minute
    time.sleep(60)
    
    Time_Series_Monthly()

# Invoke Main
main()

print('\n----STOCK DATA RETRIEVED----\n\n')

import pandas as pd
import numpy as np
import sqlite3
from sqlalchemy import create_engine
from matplotlib import pyplot as plt
import mplfinance as mpf

# Candlestick Visuals generated based on stock.txt input and filtered with SQL query for 2019-2020 Data.
# Contains secondary filtering method using Dataframe condition. 
# Visuals dumped into Data Visual folder after every iteration.
def mpf_Candlestick():
        #INPUT
        excel_file = "C:/Users/melen/Desktop/Stock_Repo/Data/Stock_YTS.xlsx"
        #Stock INPUT
        file = open('C:/Users/melen/Desktop/Stock_Repo/stocks/stocks.txt', 'r')
        #Produce data visuals for desired stocks
        for stock in file:
                # Parse Stock Symbols
                stock = stock.strip()

                # Creating sql engine to use SQL/reading Excel sheets
                engine = create_engine('sqlite://', echo=False)
                df = pd.read_excel(excel_file, sheet_name= stock)

                # Creating Tables to extract data
                df.to_sql('Monthly', engine, if_exists='replace', index=False)

                #Query1 - Filtering monthly stock data using SQL method
                q1 = engine.execute("Select * FROM Monthly \
                                WHERE DATE LIKE '%2020%' \
                                OR DATE LIKE '%2019%' \
                                ORDER BY DATE ASC \
                                ")
                monthly_Stock = pd.DataFrame(q1, columns = df.columns)

                ''' Method 2 [OPTIONAL]:
                #filter = df[(df.DATE >= '2020-01-31')]
                #filter = filter.sort_values(by=['DATE']) '''

                # Converting Date to datetime datatype and setting as index
                monthly_Stock.DATE = pd.to_datetime(monthly_Stock.DATE)
                monthly_Stock = monthly_Stock.set_index('DATE')

                # Data Visual - Candlestick chart with custom parameters
                mc = mpf.make_marketcolors(up='purple',down='Black', 
                        edge='black',
                        wick = {'up':'blue', 'down': 'red'},
                        volume='green')

                s  = mpf.make_mpf_style(marketcolors=mc, gridstyle='--', 
                        gridaxis='both', mavcolors=['red'])

                mpf.plot(monthly_Stock, type='candle', mav=(2),
                        figratio=(18,10), figscale=1.0,
                        volume=True, tight_layout=True,
                        title='['+stock+']'+ 'Monthly Time Series',
                        style=s, xrotation=20,
                        savefig='C:/Users/melen/Desktop/Stock_Repo/Data_Visuals/candles/'+stock+'.png')

# Generates Sub2Grid visual layout to merge Open, High, Low, Close, and Volume charts
def global_Visuals():
        # INPUT
        stock_data2 = pd.ExcelFile("C:/Users/melen/Desktop/Stock_Repo/Data/Stock_YTS.xlsx")
        # Dataframe used for stock iteration
        df = pd.DataFrame()

        # Subplot2grid utilized to create stock visuals
        plt.figure(figsize=(10,10))
        ax1 = plt.subplot2grid((11,1), (0,0), rowspan=2, colspan=1)
        ax1.tick_params(labelrotation=45)
        ax1.title.set_text('2020 Monthly Time Series')
        ax1.set(ylabel='Price[Close]')
        plt.grid(True)

        ax2 = plt.subplot2grid((11,1), (2,0), rowspan=5, colspan=1, sharex=ax1)
        ax2.tick_params(labelrotation=45)
        ax2.set(ylabel='Volume')
        plt.grid(True)

        ax3 = plt.subplot2grid((11,1), (7,0), rowspan=2, colspan=1, sharex=ax1)
        ax3.tick_params(labelrotation=45)
        ax3.set(ylabel='Price [Low]')
        plt.grid(True)

        ax4 = plt.subplot2grid((11,1), (9,0), rowspan=2, colspan=1, sharex=ax1)
        ax4.tick_params(labelrotation=45)
        ax4.set(ylabel='Price [High]')
        plt.grid(True)

        # Iterate multiple sheets in target excel file.
        for sheet in stock_data2.sheet_names:
                df = pd.read_excel('C:/Users/melen/Desktop/Stock_Repo/Data/Stock_YTS.xlsx', sheet_name=sheet)
                # Filtering all sheets by specific timespan usng dataframe
                filter = df[(df.DATE >= '2020-01-31')]
                filter = filter.sort_values(by=['DATE'])

                # Creating Data Visuals based on custom filter for each stock
                ax1.plot(filter.DATE, filter.Close, marker='.', markersize='5',markeredgecolor='black', linewidth='1.5', label=sheet)
                ax2.plot(filter.DATE, filter.Volume,marker='^', markersize='3',markeredgecolor='black', markerfacecolor='black',linewidth='1.5', label=sheet)
                ax3.plot(filter.DATE, filter.Low,marker='.', markersize='5',markeredgecolor='black',linewidth='1.5', label=sheet)
                ax4.plot(filter.DATE, filter.High,marker='.', markersize='5',markeredgecolor='black',linewidth='1.5', label=sheet)

                ax1.legend(bbox_to_anchor=(1.1, 1), shadow=True)
                ax2.legend(bbox_to_anchor=(1.1, .7), shadow=True)
                ax3.legend(bbox_to_anchor=(1.1, 1), shadow=True)
                ax4.legend(bbox_to_anchor=(1.1, 1), shadow=True)

        # Display/Save Visuals
        plt.subplots_adjust(hspace = .1)
        plt.savefig('C:/Users/melen/Desktop/Stock_Repo/Data_Visuals/monthly_series/monthly_series.png')
         
def main():
        # Invoke Functions
        mpf_Candlestick()
        global_Visuals()

        print('----------Data Visuals Generated----------')
        
# Invoke Main
main()


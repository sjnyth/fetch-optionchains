import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt

print()

def options_chain(symbol):
    ticker = yf.Ticker(symbol)

    # get options expiration dates
    exp_dates = ticker.options

    # get options from the expiration dates
    options = pd.DataFrame()

    for e in exp_dates:
        opt = ticker.option_chain(e)
        opt = pd.concat([opt.calls, opt.puts], axis=0)
        opt['expirationDate'] = e
        options = pd.concat([options, opt], axis=0) 

    # getting date to expiration
    options["expirationDate"] = pd.to_datetime(options["expirationDate"], format='%Y-%m-%d')
    options["dte"] = (options["expirationDate"] - dt.datetime.today()).dt.days

    # separate call options and put options
    # in the contract symbol, e.g: TSLA230707C00020000, C stands for call, P stands for put
    # 00020000 stands for strike price 20.00, 00540000 stands for strike price 540.00

    options["CALL"] = options["contractSymbol"].str[4:].apply(lambda x: True if "C" in x else False)
    options[["bid", "ask", "strike", "volume", "openInterest"]] = options[["bid", "ask", "strike", "volume", "openInterest"]].apply(pd.to_numeric)
    
    # getting mark price i.e. the mid point between bid and ask
    # theoretical price of the option 
    options["mark"] = (options["bid"] + options["ask"]) / 2
    
    # cleaning 
    options = options.drop(columns = ["contractSize", "currency", "change", "percentChange", "lastTradeDate", "lastPrice"], axis=1)
    return options

     











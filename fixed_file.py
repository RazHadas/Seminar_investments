from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import pandas as pd
import glob
from mlfinlab.labeling import raw_return
import numpy as np
import pandas as pd
%matplotlib inline
import quantstats as qs
def get_prices(df):
  x=df.columns[0]
  y=x.split("סוף יום")
  company_name=y[-1]
  d1=df.iloc[1:,:2]
  d1.columns = d1.iloc[0]
  prices=d1.iloc[1:,:]
  prices=prices.set_index('תאריך')
  prices.columns=[company_name]
  prices.index = pd.to_datetime(prices.index)
  return (prices)
def generate_outlook(t):
    df = pd.read_csv("index-125.csv", index_col=None, header=0)## read index
    d2=get_prices(df)# put index in correct way
    
    ###build dates
    w="-05-27"
    a=t+w
    x=str(pd.to_numeric(a[:4])+1)+a[4:]
    y=str(pd.to_numeric(a[:4])+2)+a[4:]
    
    ##find index returns
    index_t0=d2.loc[a:x]
    d3=index_t0.sort_index()
    returns3 =d3.iloc[:,0]
    returns3=pd.to_numeric(returns3)
    index_t0 = raw_return(prices=returns3, lag=True)
    target=qs.stats.volatility(index_t0)

    #for protfolio for t0
    d1=pd.read_csv("prices.csv",parse_dates=True, index_col="תאריך")##read data
    stocks_t0=d1.dropna(thresh=len(d1) , axis=1)
    m1 = expected_returns.mean_historical_return(stocks_t0)
    m2=m1[m1 < m1.quantile(.95)]##drop top 5%
    stocks_t0=stocks_t0[m2.index]
    stocks_t0=stocks_t0.sort_index()
    stocks_t0=stocks_t0.loc[a:x]
    stocks_t0=stocks_t0.dropna(thresh=len(stocks_t0) , axis=1)
    stocks_t0=stocks_t0.sort_index(ascending=False)

    
    S=risk_models.risk_matrix(stocks_t0,frequency=len(stocks_t0))
    mu=expected_returns.mean_historical_return(stocks_t0,frequency=len(stocks_t0))
    ef = EfficientFrontier(mu, S)
    ##target=target+0.017##use this if target is not correct
    weights = ef.efficient_risk(target_volatility=target)##build weights for EF
    ef.portfolio_performance(verbose=True)
    wei=pd.Series(weights)#change to pandas series

    
    d7=stocks_t0.pct_change().dropna()
    d7=d7[wei.index]
    returns1=wei*d7
    d8=returns1.sum(axis=1)
    portfolio_t0=d8.sort_index()
    name_index_t0="index_t0"+str(t)+".html"
    name_portfolio_t0="portfolio_t0"+str(t)+".html"
    qs.reports.html(index_t0,output=name_index_t0)
    qs.reports.html(portfolio_t0,output=name_portfolio_t0)
    
        #year t1
    df3=d1.dropna(thresh=len(d1) , axis=1)
    df3=df3.sort_index()
    stocks_t0=df3.loc[x:y]
    stocks_returns = raw_return(prices=stocks_t0,lag=True)
    new_rets=stocks_returns[wei.index]
    protfiolio=wei*new_rets
    port_t1=protfiolio.sum(axis=1)
    

    df = pd.read_csv("index-125.csv", index_col=None, header=0)
    d2=get_prices(df)
    index_t1=d2.loc[x:y]
    index_t1=index_t1.sort_index()

    returns3 =index_t1.iloc[:,0]
    returns3=pd.to_numeric(returns3)
    index_t1 = raw_return(prices=returns3, lag=True)
    
    qs.reports.metrics(port_t1,mode='full')
    name_index_t1="index_t1"+str(t)+".html"
    name_portfolio_t1="portfolio_t1"+str(t)+".html"
    name_compare_graph="compare_graph_t1"+str(t)+".html"
    qs.reports.html(index_t1,output=name_index_t1)
    qs.reports.html(port_t1,output=name_portfolio_t1)
    qs.reports.html(port_t1,index_t1,output=name_compare_graph)
generate_outlook("2018")

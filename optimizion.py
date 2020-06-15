from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
import pandas as pd
import numy as np

df=pd.read_csv("prices.csv",parse_dates=True, index_col="תאריך")##read data
df1=df.dropna(thresh=len(df) , axis=1)# delete data fo NA
df1==df2.iloc[976:,]##returns for t
df2 = df1.pct_change().dropna()##returns dataframes
returns=df2.iloc[732:976,]##returns for t+1

mu=expected_returns.mean_historical_return(df1)#genetere expected returns
S=risk_models.risk_matrix(df1)#genetere risk matrix
ef = EfficientFrontier(mu, S)

weights = ef.efficient_return(target_return=.08)
cleaned_weights = ef.clean_weights()

ef.portfolio_performance(verbose=True,risk_free_rate=0.015,freqncey=244)#calculate performance for t

wei=pd.Series(weights)
protfiolio=returns.mul(wei,axis=1)
protfiolio['total']=protfiolio.sum(axis=1)
mean_return=protfiolio['total'].mean()*244
std_return=protfiolio['total'].std()
cov_matrix1=(returns.cov())
cov_matrix=cov_matrix1*244
portfolio_vol = np.sqrt(np.dot(wei.T,np.dot(cov_matrix,weight)))
portfolio_variance=np.dot(wei.T,np.dot(log_returns.cov()*244,wei))##preformance for t+1
mean_return


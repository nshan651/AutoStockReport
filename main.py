import finviz as fv
import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import time
import requests
from datetime import date


plt.rcParams.update({'font.size': 14})
plt.xticks(rotation=25)

def price_chart(ticker):
  stock = yf.Ticker(ticker)
  hist = stock.history(period='6mo', interval='1d')
  df = pd.DataFrame(data=hist, columns=['Close'])
  df.reset_index(inplace=True)
  
  # Plot
  plt.plot(df['Date'], df['Close'], color='#800000')
  plt.title(f'{ticker} Price History')
  plt.savefig('./rif-logos/price-chart.png', bbox_inches='tight')
  #plt.close(fig1)
  
# Generic barplot
def bar_plots(df, x, y, color, title, file_name):
  fig = plt.figure(figsize = (5, 4))
  ax = sns.barplot(data=df, x=x, y=y, color=color)
  sns.despine()
  plt.bar_label(ax.containers[0])
  plt.title(title, pad=15)
  plt.savefig(file_name, bbox_inches='tight')
  plt.close(fig)
  
def stacked_bar(df, x, y1, y2, color, title, file_name):
  fig, ax = plt.subplots(figsize=(5,4))
  
  ax.bar(x, y1, color=color[0], label='Revenue')
  ax.bar(x, y2, color=color[1], bottom=y1, label='Earnings')
  
  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)
  
  plt.bar_label(ax.containers[1])
  ax.set_title(title, pad=15)
  ax.legend()
  plt.savefig(file_name, bbox_inches='tight')
  plt.close(fig)

### Driver Code ###

TICKER = 'AAPL'

#
# FINVIZ
#

# Finviz objects
stock_info = fv.get_stock(TICKER)
news = fv.get_news(TICKER)

# Reticulate global variables
PRICE = float(stock_info['Price'])
BETA = float(stock_info['Beta'])
MARKET_CAP = str(stock_info['Market Cap'])
P_E = float(stock_info['P/E'])
P_B = float(stock_info['P/B'])
EPS = float(stock_info['EPS (ttm)'])
# Remove % signs in ROE and ROI
ROE = str(stock_info['ROE'][:-1])
ROI = str(stock_info['ROI'][:-1])

# Format ticker news
STORY1_DATE=news[0][0]
STORY1_SHORT=news[0][1]
STORY1_LINK=news[0][2]

STORY2_DATE=news[1][0]
STORY2_SHORT=news[1][1]
STORY2_LINK=news[1][2]

STORY3_DATE=news[2][0]
STORY3_SHORT=news[2][1]
STORY3_LINK=news[2][2]

STORY4_DATE=news[3][0]
STORY4_SHORT=news[3][1]
STORY4_LINK=news[3][2]

STORY5_DATE=news[4][0]
STORY5_SHORT=news[4][1]
STORY5_LINK=news[4][2]

#
# YFINANCE
#

# yfinance objects
stock = yf.Ticker(TICKER)
fin = stock.financials
bal = stock.balance_sheet
cash = stock.cashflow
earn = stock.earnings
splits = stock.splits

# Global variables
SUMMARY = stock.info['longBusinessSummary']
EXACT_TIME = time.strftime('%H:%M%p %Z on %b %d, %Y')

# X-axis time series data
curr_year = int(date.today().year) 
dt = ['{}'.format(curr_year), '{}'.format(curr_year-1), '{}'.format(curr_year-2), '{}'.format(curr_year-3)]

# Create data frames
financial_data = pd.DataFrame(data=fin)
balance_data = pd.DataFrame(data=bal)
cashflow_data = pd.DataFrame(data=cash)
earnings_data = pd.DataFrame(data=earn)

# Financials
gross = [financial_data.loc['Gross Profit'][i]/1000000 for i in range(4)]
ebit = [financial_data.loc['Ebit'][i]/1000000 for i in range(4)]
debt_short = [balance_data.loc['Short Long Term Debt'][i]/1000000 for i in range(4)]
debt_long = [balance_data.loc['Long Term Debt'][i]/1000000 for i in range(4)]
revenue = [earnings_data.iloc[i][0]/1000000 for i in range(4)]
earnings = [earnings_data.iloc[i][1]/1000000 for i in range(4)]
# Derive Free Cash Flows (operating cash - capex)
operating_cash = cashflow_data.loc['Total Cash From Operating Activities']
capital_expend = cashflow_data.loc['Capital Expenditures']
fcf = []
for (op_cash, capex) in zip(operating_cash, capital_expend):
  fcf.append(op_cash/1000000 - capex/1000000)

### Save charts ###

# Financial
price_chart(TICKER)
bar_plots(financial_data, dt, gross, '#FEBD18', 'Gross Profit ($ millions)', './rif-logos/gross-profit.png')
bar_plots(financial_data, dt, ebit, '#800000', 'EBIT ($ millions)', './rif-logos/ebit.png')
# Balance sheet
bar_plots(balance_data, dt, debt_short, '#800000', 'Short Long Term Debt ($ millions)', './rif-logos/debt_short.png')
bar_plots(balance_data, dt, debt_long, '#FEBD18', 'Long Term Debt ($ millions)', './rif-logos/debt_long.png')
# Cashflow
bar_plots(cashflow_data, dt, fcf, '#FEBD18', 'Free Cash Flow ($ millions)', './rif-logos/fcf.png')
# Earnings data
stacked_bar(earnings_data, dt, revenue, earnings, ('#800000','#363636'), 'Revenue/Earnings ($ millions)', './rif-logos/revenue_earnings.png')


#!/usr/bin/env python
# coding: utf-8

# In[18]:


import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import pandas as pd
import time as tm


import matplotlib.pyplot as plt
import backtrader.analyzers as btanalyzers
import math
import numpy as np
import quantstats

# Import the backtrader platform
import backtrader as bt
import akshare as ak
#%matplotlib auto
# import telegram
# TOKEN = '1454306275:AAHbxYSgcGBoIY3t5k0BY'
# bot = telegram.Bot(TOKEN)

def get_data(code,time):
            data= ak.futures_zh_minute_sina(symbol=code, period=time)
            data['date'] = pd.to_datetime(data['date'])
            data.set_index("date",inplace=True)
            data.drop(columns=['hold'],inplace = True)
            data=data.astype({
                    'open': 'float',
                    'high':'float',
                    'low':'float',
                    'close':'float',
                    'volume':'float'
                })
            tm.sleep(1)
            return data 
        
# Create a Stratey
class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        #self.dataclose = self.datas[0].close

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None
        #print(self.data._name)
        
        self.inds = dict()
        for i, d in enumerate(self.datas):
            self.inds[d] = dict()
            # Add a MovingAverageSimple indicator
            # 50日移动平均线
            self.inds[d]['sma50'] = bt.indicators.SimpleMovingAverage(d.close,period=50)
            # 100日移动平均线
            self.inds[d]['sma100'] = bt.indicators.SimpleMovingAverage(d.close,period=100)
            # 100 日真实波动ATR
            self.inds[d]['atr100'] = bt.indicators.AverageTrueRange(d, period=100)
            # 50日的收盘最高价
            self.inds[d]['High50'] = bt.indicators.Highest(d.close(-1), period=50,subplot=False)
            # 50日的收盘最低价
            self.inds[d]['Low50'] = bt.indicators.Lowest(d.close(-1), period=50,subplot=False)

        

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        
        if self.order:
            return

        for i, d in enumerate(self.datas):
            now=datetime.datetime.now()
            now_str=now.strftime('%Y-%m-%d')
            dt_str = d.datetime.date(0).strftime('%Y-%m-%d')
            pos = self.getposition(d).size
            getcash = self.broker.getvalue()
            if not pos:  # no market / no orders
                if self.inds[d]['sma50'][0] > self.inds[d]['sma100'][0] and d.close[0] > self.inds[d]['High50'][0]:
                        cash=(0.002*getcash)/(3*self.inds[d]['atr100'][0]/d.close[0])
                        print(cash)
                        size = cash/d.close[0]
                        print(size)
                        self.order = self.buy(data=d,size = size)
                        self.log('做多品种:' + d._name + ',做多价格： %.2f' % d.close[0])
                        
                        if dt_str == now_str:
                            print("当前时间发出做多信号,正在推送TG...")
                            #bot.send_message(chat_id='727256', text="品种:%s ,价格:%.2f ,发出做多信号！" % (d._name,d.close[0]) )
                        

                if self.inds[d]['sma50'][0]  < self.inds[d]['sma100'][0] and d.close[0] < self.inds[d]['Low50'][0]:
                    cash=(0.002*getcash)/(3*self.inds[d]['atr100'][0]/d.close[0])
                    print(cash)
                    size = cash/d.close[0]
                    print(size)
                    self.order = self.sell(data=d,size = size)
        
                    self.log('做空品种:' + d._name + ',做空价格： %.2f' % d.close[0])
                    if dt_str == now_str:
                        print("当前时间发出做空信号,正在推送TG...")
                        #bot.send_message(chat_id='727256', text="品种:%s ,价格:%.2f ,发出做空信号！" % (d._name,d.close[0]) )
                        

            else :
                if self.getposition(d).size > 0  and d.close[0] < self.inds[d]['High50'][0] - 3*self.inds[d]['atr100'][0]:
                        self.order = self.close(data=d)
                        #print(self.getposition(d).size)
                        self.log('平多品种:' + d._name + ',平多价格： %.2f' % d.close[0])
                        if dt_str == now_str:
                            print("当前时间发出平多信号,正在推送TG...")
                            #bot.send_message(chat_id='7272566', text="品种:%s ,价格:%.2f ,发出平多信号！" % (d._name,d.close[0]))
                        
                
                if self.getposition(d).size < 0 and d.close[0] > self.inds[d]['Low50'][0] + 3*self.inds[d]['atr100'][0]:
                        self.order = self.close(data=d)
                        
                        self.log('平空品种:' + d._name + ',平空价格： %.2f' % d.close[0])
                        if dt_str == now_str:
                            print("当前时间发出平空信号,正在推送TG...")
                            #bot.send_message(chat_id='727256', text="品种:%s ,价格:%.2f ,发出平空信号！" % (d._name,d.close[0]))

    def stop(self):
        self.log('结束')


if __name__ == '__main__':

    # 初始化模型
    cerebro = bt.Cerebro()

    # 构建策略
    strats = cerebro.addstrategy(TestStrategy)


#     #品种池
    code_range =['C0','M0','RM0','JD0','TA0','MA0','FG0','PF0','SA0','UR0','BU0','FU0',
                 'CU0','AL0','ZN0','RB0','RU0','HC0','SP0','SS0','P0','J0','Y0','JM0','I0','AP0','CJ0',
                 'SR0','CF0']
    #code_range = ['C0','M0','A0','Y0','OI0','P0','CF0','SR0','TA0','AU0','CU0','AL0','ZN0','RB0','RU0','L0','V0']
    #code_range =['C2105','M2105','RM2105','JD2105','TA2105','MA2105','FG2105','PF2105','SA2105','UR2105','BU2106','FU2105']
    #code_range =['C2105','M2105']

    #qh_c= ak.stock_zh_a_daily(symbol="sh600000", adjust="hfq")
    #start_date = datetime.datetime(2021, 3, 8)  # 回测开始时间
    #end_date = datetime.datetime(2021, 3,30)  # 回测结束时间
    #data = bt.feeds.PandasData(dataname=qh_c, fromdate=start_date, todate=end_date)  # 加载数据
    for code_name in code_range:
        dataname = get_data(code_name,"60")
        print(dataname)
        data = bt.feeds.PandasData(dataname=dataname,timeframe=bt.TimeFrame.Minutes,compression=60)  # 加载数据
        cerebro.adddata(data,name = code_name)  # 将数据传入回测系统
    
    # 设定初始资金和佣金
    cerebro.broker.setcash(10000000.0)
    #cerebro.broker.setcommission(0.0002)
    #cerebro.addsizer(bt.sizers.PercentSizer, percents=12)

    # 以发出信号当日收盘价成交
    cerebro.broker.set_coc(True)
    # 策略执行前的资金
    print('启动资金: %.2f' % cerebro.broker.getvalue())

    # 策略执行
    #cerebro.run()
    print('结束资金: %.2f' % cerebro.broker.getvalue())
    
    stock = '601216.SH'
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name = 'sharpe')
    cerebro.addanalyzer(btanalyzers.DrawDown, _name = 'drawdown')
    cerebro.addanalyzer(btanalyzers.Returns, _name='returns')
    cerebro.addanalyzer(btanalyzers.SQN, _name='sqn')
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')




    print(f'Starte Portfolio Value {cerebro.broker.getvalue()}')
    result = cerebro.run()

    print('----------------------------')
    print(f'End portfolio value {cerebro.broker.getvalue()}')
    print('----------------------------')
    print(f"Total Return:  {round(result[0].analyzers.returns.get_analysis()['rtot']*100, 2)}%")
    print(f"APR:           {round(result[0].analyzers.returns.get_analysis()['rnorm100'],2)}%")
    print(f"Max DrawDown:  {round(result[0].analyzers.drawdown.get_analysis()['max']['drawdown'],2)}%")
    print(f"Sharpe Ratio:  {round(result[0].analyzers.sharpe.get_analysis()['sharperatio'],2)}")
    #print(f"SQN:           {round(result[0].analyzers.sqn.get_analysis()['sqn'],2)}")
    portfolio_stats = result[0].analyzers.getbyname('PyFolio')
    returns, positions, transactions, gross_lev = portfolio_stats.get_pf_items()
    returns.index = returns.index.tz_convert(None)
    quantstats.reports.html(returns, output=f'/root/{stock} Result_3.html', title=f'{stock} Analysis')
  
    #cerebro.plot(iplot=True,style = "bar",barup = "red",bardown ="green")  # 绘图


# In[ ]:





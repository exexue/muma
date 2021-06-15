#!/usr/bin/env python
# coding: utf-8

# In[5]:


#期货多品种60日线股票级别，日ATR0.02波动系统（下一个交易日开盘买入实现） Windows实现。
import datetime  # For datetime objects
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
#import akshare as ak
import os
#os.environ['DISPLAY'] = ':2'
#%matplotlib auto
import telegram
TOKEN = '****************'
bot = telegram.Bot(TOKEN)
import ths_trade

from jqdatasdk import *
auth('*****','*******') 
count=get_query_count()
print(count)



def jq_data(code,time,date):
    code =normalize_code(code)
    data = get_bars(code,count=500, unit=time,fields=['date','open','high','low','close'],include_now=True,end_dt=datetime.datetime.now(),fq_ref_date=datetime.datetime.now())
    data['date'] = pd.to_datetime(data['date'])
    data.set_index("date",inplace=True)
    tm.sleep(1)
    return data.loc[date:]

def read_csv(code,time,date):
    code =normalize_code(code)
    data = pd.read_csv("/code/data/" + time  +"/" + code)
    data['date'] = pd.to_datetime(data['date'])
    data.set_index("date",inplace=True)
    return data.loc[date:]
    
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
def Tg_send(time,code,signal,close,size):
            now=datetime.datetime.now()
            now_str=now.strftime('%Y-%m-%d')
            #now_str = "2021-05-25"
            if time == now_str:
                sizes = str(size//100*100) #计算实盘用的交易手数
                print(sizes)
                f = open('log.txt', 'r').read()
                x = "%s,code=%s,%s" % (time,code,signal)
                if x in f :
                    print("当天已经执行过了")
                else:
                    print("发出信号，正在执行实盘...")
                    os.system("python c:/ths_trade.py")  # 登录交易软件
                    position=100;close_position = 100
                    if signal == "做多":
                        position = ths_trade.buy(code,sizes)    #如果返回1说明软件中有仓位。
                        print(code)
                        print(position)
                        tm.sleep(2)
                    if signal == "平多":                                  
                        close_position = ths_trade.sell(code,sizes)   #如果返回0说明软件中无仓位。
                        tm.sleep(2)
                        
                    if position == 1 or close_position ==0:   #如果执行命令成功
                        print("实盘执行成功，当前时间发出%s信号,正在推送TG..."% (signal))
                        bot.send_message(chat_id='727256696', text="品种:%s ,价格:%.2f ,发出%s信号,实盘执行成功！" % (code,close,signal))
                        os.system('echo %s,code=%s,%s  >>log.txt' % (time,code,signal) )
                    else:
                        print("实盘执行失败，请检查软件运行情况。")
                        bot.send_message(chat_id='727256696', text="品种:%s ,价格:%.2f ,发出%s信号，但是实盘执行失败，请检查软件运行情况！" % (code,close,signal))
                        
class TestStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('{}, {}'.format(dt.isoformat(), txt))
        
        
    def __init__(self):
        self.signal = {}
        # 保存现有持仓的股票
        self.position_dict={}

        self.inds = dict()
        for d in self.datas[1:]:
            
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
 
    def prenext(self):
        #print("prenext")
        self.next()

    def next(self):
        index_date = self.datas[0].datetime.date(0).strftime('%Y-%m-%d')  #指数index当前交易日
        for d in self.datas[1:]:
            dt_str = d.datetime.date(0).strftime('%Y-%m-%d')
            pos = self.getposition(d).size
            getcash = self.broker.getvalue()
            #print(pos)
            if  pos ==0:  # no market / no orders
                if self.inds[d]['sma50'][0] > self.inds[d]['sma100'][0] and d.close[0] > self.inds[d]['High50'][0]:
                        if index_date != dt_str:     #如果指数index日期等于品种日期说明正在交易当中
                            #print("指数日期和品种日期不相等")
                            continue
                        if d._name in self.position_dict:
                            #print("已经有做多的订单了")
                            continue
                        size =(0.001*getcash)/self.inds[d]['atr100'][0]
                        #size = (getcash*0.99)/(d.close[0])
                        if math.isnan(size):  #判断size是否为nan
                            size = (getcash/len(self.datas))/(d.close[0])   #如果ATR计算失败就进行等额计算总资金/品种数目/价格
                        self.order = self.buy(data=d,size = size)
                        self.position_dict[d._name] = self.order
                        self.log('做多品种:' + d._name + ',做多价格： %.2f' % d.close[0])
                        self.signal[d._name] = [dt_str,"做多",size]
                # 已经下单，但是订单没有成交
                if d._name in self.position_dict and self.getposition(d).size==0 and self.inds[d]['sma50'][0] < self.inds[d]['sma100'][0]:
                        print("持仓为0的无效订单，取消订单,",d._name)
                        order = self.position_dict[d._name]
                        self.cancel(order)
                        self.position_dict.pop(d._name)

            else :
                if self.getposition(d).size > 0  and d.close[0] < self.inds[d]['High50'][0] - 3*self.inds[d]['atr100'][0]:
                        if d._name in self.position_dict:
                            self.order = self.close(data=d)
                            #print(self.getposition(d).size)
                            self.log('平多品种:' + d._name + ',平多价格： %.2f' % d.close[0])
                            self.position_dict.pop(d._name)
                            self.signal[d._name] = [dt_str,"平多",self.getposition(d).size]


    def notify_order(self, order):
        
        if order.status in [order.Submitted, order.Accepted]:
            return
        
        if order.status == order.Rejected:
            self.log(f"Rejected : order_ref:{order.ref}  data_name:{order.p.data._name}")
            
        if order.status == order.Margin:
            self.log(f"Margin : order_ref:{order.ref}  data_name:{order.p.data._name}")
#             try:
#                 self.position_dict.pop(order.p.data._name)
#                 print("品种下单失败，",order.p.data._name)
#             except:
#                 print("品种删除错误，",order.p.data._name)
            
        if order.status == order.Cancelled:
            self.log(f"Concelled : order_ref:{order.ref}  data_name:{order.p.data._name}")
            
        if order.status == order.Partial:
            self.log(f"Partial : order_ref:{order.ref}  data_name:{order.p.data._name}")
         
        if order.status == order.Completed:
            index_date = self.datas[0].datetime.date(0).strftime('%Y-%m-%d') 
            if order.isbuy():
                self.log(f" BUY : data_name:{order.p.data._name} price : {order.executed.price} , cost : {order.executed.value} , commission : {order.executed.comm}")                
                dt_str,signal,size = self.signal[order.p.data._name]
                Tg_send(time=index_date, code = order.p.data._name, signal = signal, close = order.executed.price, size=size)
                
            else:  # Sell
                self.log(f" SELL : data_name:{order.p.data._name} price : {order.executed.price} , cost : {order.executed.value} , commission : {order.executed.comm}")
                dt_str,signal,size = self.signal[order.p.data._name]
                Tg_send(time=index_date, code = order.p.data._name, signal = signal, close = order.executed.price, size=size)
                
    def notify_trade(self, trade):
        # 一个trade结束的时候输出信息
        if trade.isclosed:
            self.log('closed symbol is : {} , total_profit : {} , net_profit : {}' .format(
                            trade.getdataname(),trade.pnl, trade.pnlcomm))
            # self.trade_list.append([self.datas[0].datetime.date(0),trade.getdataname(),trade.pnl,trade.pnlcomm])
            
        if trade.isopen:
            self.log('open symbol is : {} , price : {} ' .format(
                            trade.getdataname(),trade.price))

    def stop(self):
        self.log('结束')
        print(self.position_dict.keys())



if __name__ == '__main__':

    # 初始化模型
    cerebro = bt.Cerebro()
    # 构建策略
    strats = cerebro.addstrategy(TestStrategy)
    #品种池

    #code_range =['510300','510300','300059','000333','000002','600519']
    #code_range =['510300','510300','513050','159920','518880','161005']
    #code_range =['510300','000333','000001','513050','513100','300059','161005','163402']
    code_range =['159915','159920','159915','510300','510500','588000','513050','163402','161005','162605','513100','159901','515650','163417','159985','159980','159981']
    #code_range =['159915','161005','159915']
 
#     dataname = read_csv('AL8888','60m','2021-03-01 10:00:00') 
#     print(dataname)
#     data = bt.feeds.PandasData(dataname=dataname,timeframe=bt.TimeFrame.Daysd,compression=1)  # 加载指数数据
#     cerebro.adddata(data,name = 'index')  # 指数数据
    for code_name in code_range:
        dataname = jq_data(code_name,"60m","2021-03-25 10:00:00")
        print(code_name)
        print(dataname)
        data = bt.feeds.PandasData(dataname=dataname,timeframe=bt.TimeFrame.Minutes,compression=60)  # 加载数据
        cerebro.adddata(data,name = code_name)  # 将数据传入回测系统

    
    print("加载数据完毕")
    # 设定初始资金和佣金
    cerebro.broker.setcash(10000.0)
    cerebro.broker.setcommission(0.0001)
    #cerebro.addsizer(bt.sizers.PercentSizer, percents=12)

    # 以发出信号当日收盘价成交
    #cerebro.broker.set_coc(True)
    # 策略执行前的资金
    print('启动资金: %.2f' % cerebro.broker.getvalue())

    # 策略执行
    #cerebro.run()
    print('结束资金: %.2f' % cerebro.broker.getvalue())
    

    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name = 'sharpe')
    cerebro.addanalyzer(btanalyzers.DrawDown, _name = 'drawdown')
    cerebro.addanalyzer(btanalyzers.Returns, _name='returns')
    cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name='track')
    cerebro.addanalyzer(bt.analyzers.PyFolio, _name='PyFolio')



    cerebro.broker.set_fundstartval(1)
    print(f'Starte Portfolio Value {cerebro.broker.getvalue()}')
    result = cerebro.run()
    print('----------------------------')
    print(f'End portfolio value {cerebro.broker.getvalue()}')
    print(cerebro.broker.get_fundvalue())
    print('----------------------------')
    print(f"Total Return:  {round(result[0].analyzers.returns.get_analysis()['rtot']*100, 2)}%")
    print(f"APR:           {round(result[0].analyzers.returns.get_analysis()['rnorm100'],2)}%")
    print(f"Max DrawDown:  {round(result[0].analyzers.drawdown.get_analysis()['max']['drawdown'],2)}%")
    trade = result[0].analyzers.track.get_analysis()
    print("总交易次数 =%s,还在交易=%s,完成的交易=%s.交易成功率百分比=%.2f ,盈亏百分比=%.2f" % 
          (str(trade['total']['total']),str(trade['total']['open']),str(trade['total']['closed']),
           trade['won']['total']/trade['total']['closed']*100,trade['won']['pnl']['average']/abs(trade['lost']['pnl']['average'])))
    
    print("连续盈利次数 = %s, 连续亏损次数= %s" % (str(trade['streak']['won']['longest']),str(trade['streak']['lost']['longest'])))
    print("总盈利次数 = %i , 总盈利 = %.2f , 平均盈利 =%.2f ,单次最大盈利 = %.2f " 
           %  (trade['won']['total'],trade['won']['pnl']['total'],trade['won']['pnl']['average'],trade['won']['pnl']['max']))
    print("总亏损次数 = %i, 总亏损 = %.2f, 平均亏损 =%.2f,单次最大亏损 = %.2f" 
           %  (trade['lost']['total'],trade['lost']['pnl']['total'],trade['lost']['pnl']['average'],trade['lost']['pnl']['max']))
    portfolio_stats = result[0].analyzers.getbyname('PyFolio')
    returns, positions, transactions, gross_lev = portfolio_stats.get_pf_items()
    returns.index = returns.index.tz_convert(None)
    transactions.index = transactions.index.tz_convert(None)
    quantstats.reports.html(returns,output=f'./data/index666.html', title=f' 期货多品种交易系统60m ATR0.001 Analysis')
  
    #cerebro.plot(iplot=True,style = "bar",barup = "red",bardown ="green")  # 绘图

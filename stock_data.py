import yfinance as yf
import mplfinance as mpf
import pandas as pd 
from datetime import date, timedelta, datetime

def get_stock_data(tickerSymbol, period, interval):
	tickerSymbol = tickerSymbol
	tickerData = yf.Ticker(tickerSymbol)
	tickerDf = tickerData.history(period=period, interval=interval)
	return tickerDf

def make_chart(stock_data):
	save = dict(fname='chart.jpg', dpi=100, bbox_inches='tight')
	s  = mpf.make_mpf_style(base_mpf_style='yahoo', gridstyle='', facecolor='#ffffff', edgecolor='#ffffff', y_on_right=False)
	mpf.plot(stock_data,type='candle', style=s, savefig=save, datetime_format='%d/%m', xrotation=0, ylabel='')

def get_today_last_info(stock_data):
	last_info = stock_data.tail(1)
	print(last_info)
	today_date = last_info.index
	today_date = today_date.strftime("%d/%m/%Y - %H:%M:%S").values[0]
	today_close_price = last_info['Close'].values[0]
	today_volume = last_info['Volume'].values[0]
	return today_date, today_close_price, today_volume

def get_day_before_info(stock_data):
	day_before = date.today() - timedelta(days=1)
	day_before_info = stock_data.loc[day_before.strftime("%Y-%m-%d")].tail(1)
	day_before_close_price = day_before_info['Close'].values[0]
	day_before_volume = day_before_info['Volume'].values[0]
	return day_before_close_price, day_before_volume

def make_message(date, today_close_price, today_volume, day_before_close_price, day_before_volume):
	prince_change_percentage = ((today_close_price - day_before_close_price)/day_before_close_price)*100
	volume_change_percentage = ((today_volume - day_before_volume)/day_before_volume)*100
	
	msg = "{} \nPreço: R${:.2f} ({:+.2f}%)".format(date,
		today_close_price,prince_change_percentage)
	return msg

if __name__ == '__main__':
	stock_data = get_stock_data('IRBR3.SA', '5d', '60m')
	print(stock_data)
	make_chart(stock_data)
	today_date, today_close_price, today_volume = get_today_last_info(stock_data)
	day_before_close_price, day_before_volume = get_day_before_info(stock_data)
	msg = make_message(today_date, today_close_price, today_volume, day_before_close_price, day_before_volume)
	print(msg)


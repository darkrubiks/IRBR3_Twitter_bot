import tweepy
import time
from stock_data import *
from datetime import date, timedelta, datetime

# Authenticate to Twitter

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

now = datetime.now()

hour_10 = now.replace(hour=10)
hour_11 = now.replace(hour=11)
hour_12 = now.replace(hour=12)
hour_13 = now.replace(hour=13)
hour_14 = now.replace(hour=14)
hour_15 = now.replace(hour=15)
hour_16 = now.replace(hour=16)

while now <= hour_16:
	if now >= (hour_10 or hour_11 or hour_12 or hour_13 or hour_14 or hour_15):
		print('getting data ', now.strftime("%H:%M:%S"))
		try:
			api.verify_credentials()
			print("Authentication OK")
			stock_data = get_stock_data('IRBR3.SA', '5d', '60m')
			make_chart(stock_data)
			today_date, today_close_price, today_volume = get_today_last_info(stock_data)
			day_before_close_price, day_before_volume = get_day_before_info(stock_data)
			msg = make_message(today_date, today_close_price, today_volume, day_before_close_price, day_before_volume)
			msg = msg + "\n#IRBR3 #ações #investimentos #ibovespa #bot"
			print("Posting")
			api.update_with_media("C:\\Users\\leona\\Desktop\\IRBR3_twitter_bot\\chart.jpg", status=msg)
		except:
			print("Error during authentication")


	else:
		print('closed market')

print('closed market, ending program')

import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import sched, time
import yagmail

tickers = open('C://Users//steph//temp//macd_tickers.txt', 'r').readlines()
#tickers = ['AAPL']
tickers = [line.rstrip() for line in tickers]

buy_alerts = []
sell_alerts = []


def screen_macd():

    today_date = datetime.today().date()

    if datetime.today().date().weekday() == 0:

        yest_date = today_date - timedelta(days=3)

    else:
        yest_date = today_date - timedelta(days=1)

    today_date = str(today_date)
    yest_date = str(yest_date)

    print(today_date)
    print(yest_date)
    print("Starting AlphaVantage scrape...")

    counter = 0

    for ticker in tickers:
        print(ticker)

        if counter >= 5:
            time.sleep(60)
            counter = 0

        r = requests.get(f'https://www.alphavantage.co/query?function=MACD&symbol={ticker}&interval=daily&series_type=close&apikey=NFHEH6FP1B2G4INP')
        content = json.loads(r.text)
        counter += 1

        try:
            hist_today = content.get('Technical Analysis: MACD').get(today_date).get('MACD_Hist')
            hist_yesterday = content.get('Technical Analysis: MACD').get(yest_date).get('MACD_Hist')

            print(ticker + " Today: " + hist_today + " Yest: " + hist_yesterday)

            if float(hist_today) * float(hist_yesterday) < 0:
                if float(hist_today) > 0:
                    buy_alerts.append(ticker)
                else:
                    sell_alerts.append(ticker)

        except AttributeError:
            pass

    print("Scrape finished.")

def send_email():

    re = "MACD Crossovers for " + str(today_date)
    body = "Buy alerts: " + str(buy_alerts)  + "\nSell alerts:" + str(sell_alerts)

    yag = yagmail.SMTP('{YOUR GMAIL}', '{YOUR PASSWORD}}')

    yag.send(
        to="{YOUR RECIPIENT}",
        subject= re,
        contents=body
            )
    print("Email sent!")

screen_macd()
send_email()

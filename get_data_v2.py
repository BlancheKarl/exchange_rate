from pathlib import Path
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')
import os
import datetime
import time
import json
from apscheduler.schedulers.background import BackgroundScheduler

def get_data(url, headers):
    pd.set_option('colheader_justify', 'center')
    req = requests.get(url=url, headers=headers)
    # tex = req.text
    soup = BeautifulSoup(req.text, 'lxml')
    body = soup.find_all(width='600',bgcolor='#EAEAEA')[0].find_all('tr')
    s = []
    for  j  in range(len(body)):
        if j == 0:
            j += 1
        currency_name = body[j].text.split('\n')[1]
        buying_rate = body[j].text.split('\n')[2]
        selling_rate = body[j].text.split('\n')[4]
        if buying_rate != "" and selling_rate !="":

            one = {}
            one['currency_name'] = currency_name
            one['buying_rate'] = buying_rate
            one['selling_rate'] = selling_rate
            s.append(one)
    return s
def exchange_rate():
    head ={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}
    url = 'https://www.bankofchina.com/sourcedb/whpj/enindex_1619.html'
    result  = get_data(url, head)


    with open('data.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(result, indent=2, ensure_ascii=False))
    time.sleep(10)


if __name__ == '__main__':
    #scheduler = BackgroundScheduler()
    #add task with interval of 2 seconds
    #scheduler.add_job(exchange_rate, 'interval', seconds=5)
    #scheduler.start()

    while True:
        exchange_rate()
        print(time.time())
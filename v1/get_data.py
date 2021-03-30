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
from apscheduler.schedulers.background import BackgroundScheduler

def get_data(url, headers):
    pd.set_option('colheader_justify', 'center')
    req = requests.get(url=url, headers=headers)
    # tex = req.text
    soup = BeautifulSoup(req.text, 'lxml')
    body = soup.find_all(width='600',bgcolor='#EAEAEA')[0].find_all('tr')
    s = []
    for  j  in range(len(body)):
        a = [i for i in body[j].text.split('\n')]
        s.append(a)
    data = pd.DataFrame(s[1:],columns=s[0])
    return data

def exchange_rate():
    head ={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}
    url = 'https://www.bankofchina.com/sourcedb/whpj/enindex_1619.html'
    df  = get_data(url, head)

    pd.set_option('colheader_justify', 'center')  # FOR TABLE <th>
    html_string = '''
        <html>
          <head><title>Exchange Rate</title></head>
          <link rel="stylesheet" type="text/css" href="df_style.css"/>
          <body>
            {table}
          </body>
        </html>.
        '''
    # OUTPUT AN HTML FILE
    with open('myhtml.html', 'w') as f:
        f.write(html_string.format(table=df.to_html(classes='mystyle')))

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    #add task with interval of 2 seconds
    scheduler.add_job(exchange_rate, 'interval', seconds=20)
    scheduler.start()

    while True:
        print(time.time())
        time.sleep(5)
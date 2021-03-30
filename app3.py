from flask import Flask, jsonify
import pandas as pd
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')
import time
import json
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler
import json
import pymysql
from flask import render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)

def get_data():
    exrate = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'}
    url = 'https://www.bankofchina.com/sourcedb/whpj/enindex_1619.html'
    pd.set_option('colheader_justify', 'center')
    req = requests.get(url=url, headers=headers)
    # tex = req.text
    soup = BeautifulSoup(req.text, 'lxml')
    body = soup.find_all(width='600', bgcolor='#EAEAEA')[0].find_all('tr')
    s = []
    for j in range(len(body)):
        if j == 0:
            j += 1
        currency_name = body[j].text.split('\n')[1]
        buying_rate = body[j].text.split('\n')[2]
        selling_rate = body[j].text.split('\n')[4]
        if buying_rate != "" and selling_rate != "":
            one = {}
            one['currency_name'] = currency_name
            one['buying_rate'] = buying_rate
            one['selling_rate'] = selling_rate
            exrate.append(one)
    return exrate

#@app.route('/todo/api/v1.0/exrate', methods = ['GET'])
#def get_exrate():
#   return jsonify({'exchange_rate':exrate})

@app.route('/todo/api/v1.0/exrate', methods = ['GET'])
def get_exrate():
    exrate = get_data()
    with open('data.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(exrate, indent=2, ensure_ascii=False))
    return jsonify({'exchange_rate':exrate})

@app.route('/')
def index():
    conn = pymysql.connect(host='localhost', user='root', password='lizheng980316',port=3306, db='xdb', charset='utf8')
    cur = conn.cursor()
    sql = "SELECT * FROM xdb.exchange_rate"
    cur.execute(sql)
    u = cur.fetchall()
    conn.close()
    return render_template('Homepage.html', u=u)

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    # add task with interval of 2 seconds
    scheduler.add_job(get_exrate, 'interval', seconds=100)
    scheduler.start()
    app.run(debug=False)




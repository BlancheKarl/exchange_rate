from flask import Flask, jsonify
import pandas as pd
import requests
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings('ignore')
from apscheduler.schedulers.background import BackgroundScheduler
import json
import pymysql
from flask import render_template



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

def json2db():
    conn = pymysql.connect(
        host='localhost',  # mysql服务器地址
        port=3306,  # 端口号
        user='root',  # 用户名
        passwd='lizheng980316',  # 密码
        db='xdb',  # 数据库名称
        charset='utf8',  # 连接编码，根据需要填写
    )
    cur = conn.cursor()  # 创建并返回游标

    cur.execute('DROP TABLE IF EXISTS exchange_rate')

    # 创建表头
    sql = "CREATE TABLE exchange_rate (currency_name  VARCHAR(32),buying_rate  VARCHAR(100),selling_rate VARCHAR(100));"
    cur.execute(sql)
    conn.commit()
    a = open(r"data.json", "r", encoding='UTF-8')
    out = a.read()
    tmp = json.dumps(out)
    tmp = json.loads(out)
    num = len(tmp)
    i = 0
    while i < num:
        currency_name = tmp[i]['currency_name']
        buying_rate = tmp[i]['buying_rate']
        selling_rate = tmp[i]['selling_rate']
        value = [currency_name, buying_rate, selling_rate]
        sql_insert = "insert into exchange_rate (currency_name, buying_rate, selling_rate) values (" + "'" + currency_name + "'" + "," + "'" + buying_rate + "'" + "," + "'" + selling_rate + "'" + ");"
        # sql_insert =("insert into daxue (code,charge,level,name,remark,prov) values (%s,%s,%s,%s,%s,%s);",value)
        # sql_insert = sql_insert.encode("utf8")
        print(sql_insert)

        cur.execute(sql_insert)  # 执行上述sql命令
        i = i + 1

    # print(num)
    conn.commit()
    conn.close()

@app.route('/todo/api/v1.0/exrate', methods = ['GET'])
def get_exrate():
    exrate = get_data()
    with open('data.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(exrate, indent=2, ensure_ascii=False))
    json2db()
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

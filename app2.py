from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
import pymysql

app = Flask(__name__)
bootstrap = Bootstrap(app)


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
    app.run(debug=True)


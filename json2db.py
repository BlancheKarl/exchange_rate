import json
import pymysql


conn = pymysql.connect(
        host = 'localhost',#mysql服务器地址
        port = 3306,#端口号
        user = 'root',#用户名
        passwd = 'lizheng980316',#密码
        db = 'xdb',#数据库名称
        charset = 'utf8',#连接编码，根据需要填写
    )
cur = conn.cursor()#创建并返回游标

#创建表头
#sql = "CREATE TABLE exchange_rate (currency_name  VARCHAR(32),buying_rate  VARCHAR(100),selling_rate VARCHAR(100));"

#cur.execute(sql)#执行上述sql命令
a = open(r"data.json", "r",encoding='UTF-8')
out = a.read()
tmp = json.dumps(out)
tmp = json.loads(out)
num = len(tmp)
i = 0
while i < num:
    currency_name = tmp[i]['currency_name']
    buying_rate = tmp[i]['buying_rate']
    selling_rate = tmp[i]['selling_rate']
    value = [currency_name,buying_rate,selling_rate]
    sql_insert = "insert into exchange_rate (currency_name, buying_rate, selling_rate) values (" + "'"+currency_name+"'" +","+ "'"+buying_rate+"'" + ","+"'"+selling_rate+"'" + ");"
    # sql_insert =("insert into daxue (code,charge,level,name,remark,prov) values (%s,%s,%s,%s,%s,%s);",value)
    # sql_insert = sql_insert.encode("utf8")
    print(sql_insert)

    cur.execute(sql_insert)  # 执行上述sql命令
    i = i+1

# print(num)
conn.commit()
conn.close()
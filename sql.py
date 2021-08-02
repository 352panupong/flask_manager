from flaskext.mysql import MySQL
from flask import Flask, render_template, make_response, request, redirect


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'backoffice'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'bluehouse'
mysql = MySQL(app)

mysql.init_app(app)



def expendToMysql(conn,date_,detail,price_,ect,account_id_):
    cur = conn.cursor()
    print(date_)
    print(detail)
    print(price_)
    print(ect)
    print(account_id_)


    cur.execute("INSERT INTO account(date_at,detail,price,detail_more,account_id_account_id) VALUES ('%s','%s',%s,'%s',%s);"% (date_,detail,price_,ect,account_id_,)) 

    conn.commit()
    cur.close()
    print('correct')
    return 

def incomeToMysql(conn,date,detail,weight,price,more,account_id):
    cur = conn.cursor()
    print(date)

    cur.execute("INSERT INTO account(date_at,detail,weight,price,detail_more,account_id_account_id) VALUES ('%s','%s',%s,%s,'%s',%s);"% (date,detail,weight,price,more,account_id,))
    conn.commit()
    cur.close()
    print('correct')
    return 

def SelectAccount(conn):
    cur = conn.cursor()

    cur.execute("SELECT SUM(price) FROM account WHERE account_id_account_id = 1 AND month(date_at) = MONTH(CURRENT_TIMESTAMP);")

    Account =  cur.fetchall()
    
    if Account == None:
        print('0')
        Account = 0
        print(Account)
    return Account

def SelectIncome(conn):
    cur = conn.cursor()

    cur.execute("SELECT SUM(price),SUM(weight) FROM account WHERE account_id_account_id = 2 AND month(date_at) = MONTH(CURRENT_TIMESTAMP);")

    income =  cur.fetchall()
    if income == None:
        print('0')
        income = 0
        print(income)
    return income

def InsertReport(conn,date,report):
    cur = conn.cursor()
    

    cur.execute("INSERT INTO report(date_at,detail) VALUES ('%s','%s');"% (date,report,))
    conn.commit()
    cur.close()
    print('correct')
    return 

def SelectReport(conn):
    cur = conn.cursor()

    cur.execute("SELECT DATE(date_at),detail FROM report WHERE month(date_at) = MONTH(CURRENT_TIMESTAMP) ORDER BY date_at DESC;")

    income =  cur.fetchall()
    return income

def SelectReportByDate(conn,date_befor,date_after):
    cur = conn.cursor()

    cur.execute("SELECT DATE(date_at),detail FROM report WHERE (Date_at BETWEEN '%s' AND '%s') ORDER BY date_at DESC;"%(date_befor,date_after,))

    report =  cur.fetchall()
    return report

def CheckUser(conn,username,password):
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_id ")

    UserLogin = cur.fetchall()
    print(UserLogin)
    for user in  UserLogin:
        

        if username == user[1] and password == user[2]:
            print(user[3])
            status = user[3]
            return status
        else:
            status = 'incorrect'
            return status

def InsertWaterOne(conn,status):
    cur = conn.cursor()
    print(status)

    cur.execute("Update sensor_status SET status_sensor = '%s' Where id_sensor_status = 1;"% (status,))
    conn.commit()
    cur.close()
    print('correct')
    return 

def InsertWaterTwo(conn,status):
    cur = conn.cursor()
    print(status)

    cur.execute("Update sensor_status SET status_sensor = '%s' Where id_sensor_status = 2;"% (status,))
    conn.commit()
    cur.close()
    print('correct')
    return 

def InsertWaterThree(conn,status):
    cur = conn.cursor()
    print(status)

    cur.execute("Update sensor_status SET status_sensor = '%s' Where id_sensor_status = 3;"% (status,))
    conn.commit()
    cur.close()
    print('correct')
    return    


def InsertFogOne(conn,status):
    cur = conn.cursor()
    print(status)

    cur.execute("Update sensor_status SET status_sensor = '%s' Where id_sensor_status = 4;"% (status,))
    conn.commit()
    cur.close()
    print('correct')
    return    

def InsertFogTwo(conn,status):
    cur = conn.cursor()
    print(status)

    cur.execute("Update sensor_status SET status_sensor = '%s' Where id_sensor_status = 5;"% (status,))
    conn.commit()
    cur.close()
    print('correct')
    return 

def InsertFogThree(conn,status):
    cur = conn.cursor()
    print(status)

    cur.execute("Update sensor_status SET status_sensor = '%s' Where id_sensor_status = 6;"% (status,))
    conn.commit()
    cur.close()
    print('correct')
    return 

def moniterData(conn):
    cur = conn.cursor()
    
    cur.execute("SELECT val FROM value order by dt desc limit 4 ")
    Value =  cur.fetchall()

    return Value
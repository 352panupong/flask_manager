from flask import Flask, render_template, make_response, request, redirect,session
from flaskwebgui import FlaskUI #get the FlaskUI class
from wtforms import SelectField
from flask_wtf import FlaskForm
from flaskext.mysql import MySQL
from flask_json import FlaskJSON, JsonError, json_response, as_json
import paho.mqtt.client as mqtt
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_login import login_manager, login_required, logout_user
from sql import *

# from connect import *
import xml.etree.ElementTree as ET
import os 
import io
import datetime
# import mysql.connector
# import psycopg2 as p

host = "192.168.110.70"
port = 1885

app = Flask(__name__)
# # app.config['SECRET_KEY'] = 'cairocoders-ednalan'
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://backoffice:password@localhost/backoffice"
mysql = MySQL()
app.config['SECRET_KEY'] = 'secret'
app.config['MYSQL_DATABASE_USER'] = 'backoffice'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'bluehouse'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'


mysql.init_app(app)
conn = mysql.connect()

ui = FlaskUI(app)
 
#  login control

@app.route('/log',methods= ['GET','POST'])
def index():
    return  render_template("login/logi.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    username = str(request.args.get('username'))
    Log_password = str(request.args.get('Log_password'))
    status = CheckUser(conn,username,Log_password)
    session['status'] = status

    if status == 'admin':
        return redirect('/index')

    elif status == 'incorrect':
        return redirect('/')


@app.route("/logout")
def logout():
    
    return redirect('/')

# endLogin


# start dashboard index

@app.route('/controlWaterOne',methods=['POST', 'GET'])
def controlWaterOne():
    data_one = str(request.args.get('WaterControlOne'))
    print(data_one)
    InsertWaterOne(conn,data_one)
    return data_one

@app.route('/controlWaterTwo',methods=['POST', 'GET'])
def controlWaterTwo():
    data_two = str(request.args.get('WaterControlTwo'))
    print(data_two)
    InsertWaterTwo(conn,data_two)
    return data_two

# @app.route('/controlWaterThree',methods=['POST', 'GET'])
# def controlWaterThree():
#     data_three = str(request.args.get('WaterControlThree'))
#     print(data_three)
#     InsertWaterTwo(conn,data_three)
#     return data_three


@app.route('/controlFogOne',methods=['POST', 'GET'])
def controlFogOne():
    fog_one = str(request.args.get('FogControlOne'))
    print(fog_one)
    InsertFogOne(conn,fog_one)
    return fog_one

@app.route('/controlFogTwo',methods=['POST', 'GET'])
def controlFogTwo():
    fog_two = str(request.args.get('FogControlTwo'))
    print(fog_two)
    InsertFogTwo(conn,fog_two)
    return fog_two

@app.route('/controlFogThree',methods=['POST', 'GET'])
def controlFog():
    fog_three = str(request.args.get('FogControlThree'))
    print(fog_three)
    InsertFogThree(conn,fog_three)
    return fog_three

@app.route('/')
def start():
    # connect_mqtt = connect_mqtt_()
    # return render_template("input.html")
    # value = moniterData(conn)
    # print(value)
    return render_template("dashboard/graph.html")


@app.route('/realtime')
def realtime():
    value = moniterData(conn)
    print(value)
    result = 'data'
    for val in value:
        print(val)
        
        value = str(val[0])
        # sensor    = ' '+str(val[1])
        result = result + ' ' +value
    
        
    print(result)
    return result
# end dashboard index



# start Finance

@app.route('/expend')
def SaveTo():
    # cur = mysql.connection.cursor()

    date_to = str(request.args.get('Date_only'))
    Detail = str(request.args.get('Detail'))
    Price = int(request.args.get('price'))
    ect_ = str(request.args.get('ect'))
    account_id = int(request.args.get('account_id'))
    if date_to =="":
        date_to = datetime.datetime.now()
    
    expend_to = expendToMysql(conn,date_to,Detail,Price,ect_,account_id)
    # print(expend_to)
    #เอาค่าไปลง database สร้างอีกอันนึง
    return redirect('/finance')


@app.route('/revenue')
def revenue():
    # cur = mysql.connection.cursor()

    revenue_date = str(request.args.get('revenue_date'))
    revenue_detail = str(request.args.get('revenue_detail'))
    revenue_weight = int(request.args.get('revenue_weight'))
    revenue_price = int(request.args.get('revenue_price'))
    revenue_more = str(request.args.get('revenue_more'))
    revenue_account_id = str(request.args.get('account_id_re'))
   
    
    #เอาค่าไปลง database สร้างอีกอันนึง
    if revenue_date =="":
        revenue_date = datetime.datetime.now()

    incomeToMysql(conn,revenue_date,revenue_detail,revenue_weight,revenue_price,revenue_more,revenue_account_id)

    return redirect('/finance')
    
@app.route('/finance')
def finance():
    expendAcc = SelectAccount(conn)
    income = SelectIncome(conn)
    print(expendAcc)
    print(income)

    
    for expend in expendAcc:
        if expend[0] == None:
            sum_Acc = 0
        
        else:
            for come in income:
                if come[0] == None:
                    sum_Acc = 0 - expend[0]
                else:
                    sum_Acc = come[0] -expend[0]

    
    # for expend in expendAcc:
    #     for in_come in income:
    #            sum_Acc = in_come[0] - expend[0]
    
    # print(sum_Acc)
    return render_template("finance/inputAcc.html",Account = expendAcc, income = income,sum_Acc=sum_Acc)

# end finanece



# start MQTT connect

def on_connect(self, client, userdata, rc): #connect server and config topic
    print("MQTT Connected")
    self.subscribe("testPaho")
    self.publish("testPaho","sendTest")
    return

def on_message(client, userdata,msg): #receive when publish update
    message = msg.payload.decode("utf-8","strict")
    print(message)


# end mqtt connect



# start report   

@app.route('/report')
def report():
    Report = SelectReport(conn)
    print(Report)
    table = 'main'
    
    return render_template("report/report_table.html",Report = Report,table=table)

@app.route('/report_sub')
def report_sub():
    date_report = str(request.args.get('date_report'))
    report = str(request.args.get('report'))

    InsertReport(conn,date_report,report)
    print(date_report)
    print(report)

    return redirect('/report')
    
@app.route('/searchReport')
def searchReport():
    date_befor = str(request.args.get('date_report_befor'))
    date_after = str(request.args.get('date_report_after'))

    data = SelectReportByDate(conn,date_befor,date_after)
    table = 'search'

    return render_template("report/report_table.html",Report = data,table=table)

# end report

if __name__ == '__main__':
    print("start")
    # client = mqtt.Client()
    # client.on_connect = on_connect
    # client.on_message = on_message
    # client.connect(host,port)

    # client.loop_start()

    ui.run()
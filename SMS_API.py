from flask import Flask,request,jsonify
import sqlite3
from flask_cors import CORS
import config
import os
from twilio.rest import Client


app = Flask(__name__)
CORS(app)

DATABASE_NAME = os.getenv("DATABASE_NAME")
account_sid = os.getenv('account_sid')
auth_token = os.getenv('auth_token')

@app.route('/get_companies' , methods = ['GET'])
def get_companies():
     conn = sqlite3.connect(DATABASE_NAME)
     cursor = conn.cursor()
     cursor.execute("SELECT name FROM companies")
     companies_name = cursor.fetchall()
     conn.commit()
     conn.close()
     return(jsonify({'companies_name': companies_name}))


@app.route('/get_investores/<company>',methods = ['GET'])
def get_investores(company):
     conn = sqlite3.connect(DATABASE_NAME)
     cursor = conn.cursor()
     if (company == 'None'):
        cursor.execute("SELECT * FROM investores")
     else:
        cursor.execute("SELECT id FROM companies WHERE name = ?",(company,))
        company_id = cursor.fetchall()[0][0]
        cursor.execute("SELECT * FROM investores WHERE company_id = ? ",(company_id,))

     investores = cursor.fetchall()
     conn.commit()
     conn.close()
     return(jsonify({'investores_info': investores}))


@app.route('/send_sms/<company>/<investor>',methods=['POST'])
def send_sms(company,investor):
    if(investor == 'None'):
        investors = get_investores(company)
        data = investors.get_json()
        investor_info = data.get('investores_info')


    else:
       conn = sqlite3.connect(DATABASE_NAME)
       cursor = conn.cursor() 
       print(type(investor))
       cursor.execute("SELECT * FROM investores WHERE investor_number = ?",(investor,))
       investor_info = cursor.fetchall()
       print("i am here")
    print(investor_info)
    messages = []
    for i in investor_info:
       name  = i[2]
       phone_number = i[3]
       number = i[4]
       msg_tempalte = 'Dear ' + name + ' associated with ' + company + ' company ' +' This is your investor number ' + number  
       messages.append((phone_number,msg_tempalte))
       """
     client = Client(account_sid, auth_token)
     for i in messages:
       message = client.messages.create(
       body=messages[1],
       from_='+1234567890',
       to = messages[0]
       )
       

       print(f"Message sent with SID: {message.sid}")
       """
    print(messages)
    return(jsonify({'messages': messages}))



if __name__ == '__main__':
    config.init_db() 
    app.run(debug = True)


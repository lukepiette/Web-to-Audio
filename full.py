#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8
# export FLASK_APP=test_
# flask run
# http://127.0.0.1:5000/
# export FLASK_ENV=development
# app = Flask(__name__,template_folder='templates',static_folder='static')
# href="{{ url_for('static',filename='css/plugins.css') }}"
# app.config['DEBUG'] = True

                # <form action="" method="post">
                # <input type="file" name="pic" accept="image/*">
                # </form>
            
#db.child("names").push({"name":"Luke"})
#db.child("usernames").child("user1").update({"name":"Paul"})
#db.child("user").update({"name":"PAUUUL"})
#db.child("user").child("name").remove()
#username.key()
#username.val()
#db.child("user").child("name").remove()
#.getChildrenCount()
 
# ----------------------
#db.child(random).update({"email":"lukewpiette@gmail.com"})
#db.child(random).update({"first-name":"Luke"})
#db.child(random).update({"last-name":"Piette"})
#db.child(random).update({"password":"piette2000"})
# -----------------------

#db.child("user-info").child("lukesspiette@gmail.com").set({"first-name":"luke"})
#db.child("user").child("lukewpiette@gmail.com")
#userdata = db.child("user").child(username)
#username = db.child("user").get()


from flask import Flask, escape, url_for, request, render_template, redirect
from flask_mysqldb import MySQL
import pyautogui
import time
import random
import string
import pygame
import hashlib
import cv2
import os
from werkzeug.utils import secure_filename
import logging
import pymysql
import pyrebase
import datetime
import html

config = {
    "apiKey": "AIzaSyDZtNGBKrJ4jasYwk9fIbHhawQRDeCdrmQ",
    "authDomain": "disrupt-project.firebaseapp.com",
    "databaseURL": "https://disrupt-project.firebaseio.com",
    "projectId": "disrupt-project",
    "storageBucket": "disrupt-project.appspot.com",
    "messagingSenderId": "926375683346",
    "appId": "1:926375683346:web:be91bb5c229cc81136ffcb"}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()

ID = None
user = ''

app = Flask(__name__,template_folder='templates',static_folder='static')
mysql = MySQL(app)



@app.route('/login',methods=['GET', 'POST'])
def login():
    global ID
    if request.method == 'POST':
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        
        box = []
        ids = []
        inventory = db.get()
        for business in inventory.each():
            box += [business.val()]
            ids += [business.key()]
                
        for i in range(len(box)):
            if box[i]['email'] == email and box[i]['password'] == password:
                ID = ids[i]
                return redirect(url_for('dashboard'))
            else:
                return render_template('login.html')
        
    return render_template('login.html')


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
    global user
    
    month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
    box = []
    times = []

    try:
        inventory = db.child(ID).get()
        for business in inventory.each():
            box += [business.val()]

        for i in box[0]:
            dd = box[0][i]['last-meeting'].split('-')
            month = int(dd[1])-1
            days = int(dd[2])
            for o in range(len(month_days[:month])):
                days += month_days[o]
            curr_month = int(str(datetime.datetime.now())[0:10].split('-')[1])-1
            curr_day = int(str(datetime.datetime.now())[0:10].split('-')[2])
            for w in range(len(month_days[:curr_month])):
                curr_day += month_days[w]

            time_since = curr_day-days

            times += [time_since]

        num_lis = [0,0,0,0]
        for i in times:
            if i >= 30:
                num_lis[-1] += 1
            for o in range(4):
                if o*10 <= i < (o+1)*10:
                    num_lis[o] += 1

        if request.method == 'POST':
            try:
                user = request.form.get('search-result', None)
                return redirect(url_for('results'))
            except:            
                first_name = request.form.get('first-name', None)
                last_name = request.form.get('last-name', None)
                linkedin_URL = request.form.get('linkedin-url', None)
                email = request.form.get('email', None)

                current_date = str(datetime.datetime.now())[0:10]

                db.child(ID).child('connections').update({first_name+" "+last_name: {'email':email,'linkedin':linkedin_URL,'title':' ','note':'','last-meeting':current_date,'meeting':{'none':''}}})

        return render_template('dashboard.html',num1=num_lis[0],num2=num_lis[1],num3=num_lis[2],num4=num_lis[3])
    except TypeError:
        return('404 page not found.\n\nLog in to continue.')
    

    
@app.route('/results',methods=['GET', 'POST'])
def results():
    global user
        
    color_gradients = ['#a3f48f','#bbf48f','#d4f48f','#e0f48f','#f2f48f','#f4bf8f','#F48F98']
    month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
    
    box = []
    inventory = db.child(ID).get()
    for business in inventory.each():
        box += [business.val()]

    count = 0
    names = []
    emails = []
    linkedins = []
    titles = []
    dates = []
    color = []
    bar_pos = []
    div_tag = ''

    for i in box[0]:
        count += 1
        names += [i]
        emails += [box[0][i]['email']]
        linkedins += [box[0][i]['linkedin']]
        titles += [box[0][i]['title']]

        dd = box[0][i]['last-meeting'].split('-')
        month = int(dd[1])-1
        days = int(dd[2])
        for o in range(len(month_days[:month])):
            days += month_days[o]

        curr_month = int(str(datetime.datetime.now())[0:10].split('-')[1])-1
        curr_day = int(str(datetime.datetime.now())[0:10].split('-')[2])

        for w in range(len(month_days[:curr_month])):
            curr_day += month_days[w]

        time_since = curr_day-days
        dates += [time_since]

        for cc in range(7): 
            if (cc)*6 <= time_since < (cc+1)*6:
                color += [color_gradients[cc]]

        bar_t = -80+time_since*2
        if bar_t > -10:
            bar_t = -10
        bar_pos += [bar_t]
   
    for i in range(count):
        if user.lower() in names[i].lower():
            div_tag += '<a href="connection-profile/{}">'.format(names[i])
            div_tag += "<div><div id='{}' class='card shadow border-left-warning py-2' style='margin-left: 0px;/*margin-right: 0%;*/height: 100px;border-left: 1px solid #e3e6f0;margin-bottom: 20px;background-color: rgb(251,251,251);/*border: 1px transparent;*/border: 1px solid transparent;border-left: .01rem solid white!important;max-width: 350px;'><div class='card-body' style='margin-top: -12px;/*border: 1px solid transparent;*/height: 100px;'><input onclick='checkBoxCheckedGood({})'".format(("connection-"+str(i+1)),str(i))
            div_tag += "type='checkbox' style='position: absolute;left: -30px;top: 42%;/*border: 1px solid black;*/background-color: black !important;filter: blur(0px) brightness(118%);font-size: 81px;width: 17px;'><div class='row align-items-center no-gutters'><div class='col' style='cursor:pointer;'><img src='assets/img/luke.png' style='width: 70px;border-radius: 50%;display: inline-block;float: left;max-height: 70px;object-fit: cover;position: relative !important;'><p style='padding-left: 10px;display: inline-block;float: left;font-family: sans-serif;font-weight: normal;padding-top: 9px;font-size: 25px;color: rgb(6,6,6);'>{}</p>".format(names[i])
            div_tag += "<p style='padding-left: 10px;display: inline-block;float: left;clear: left;margin-top: -28px;margin-left: 72px;font-size: 11px;font-family:sans-serif;font-weight: normal;color: rgb(89,89,89);'>{}</p>".format(titles[i])
            div_tag += "<p style='position: absolute;right: -135px;top: 25px;color: rgb(190,190,190);font-weight: bold;'>{}</p><a href='{}' target='blacnk'><i class='fa fa-linkedin-square' style='position: absolute;right: 0;top: 12%;font-size: 22px;color: #e2e2e2;'></i></a>".format(dates[i],linkedins[i])
            div_tag += "<a href='{}'><i class='material-icons' style='position: absolute;right: -2px;top: 54%;font-size: 22px;color: #e2e2e2;'>mail_outline</i></a></div></div><div style='position: absolute;height: 30px;width: 150px;right: -90px;top: 38%;bottom: 60%;border-radius: 15px 15px 15px 15px;background-color: white;z-index: -1;border: 2px solid #e2e2e2;'></div><div style='position: absolute;height: 30px;width: 150px;right: {}px;top: 38%;bottom: 60%;border-radius: 15px 0px 0px 15px;background-color: {};z-index: -1;border: 1px solid #e2e2e2;'></div></div></div></div></a>".format(emails[i],str(bar_pos[i]),color[i])

    if request.method == 'POST':
        try:
            user = request.form.get('search-result', None)
            return redirect(url_for('results'))
        except:
            if len(request.form.get('inside-text', None)) > 0:
                note_content = request.form.get('inside-text', None).split("|")
                name = note_content[0]
                note = note_content[1]
                loc = db.child(ID).child('connections').child(name).child('meeting').get()
                count = 0
                for c in loc.each():
                    count += 1
                for j in names:
                    if j == name:
                        current_date = str(datetime.datetime.now())[0:10]
                        db.child(ID).child('connections').child(name).child('meeting').update({current_date:note})
                        db.child(ID).child('connections').child(name).update({'last-meeting':current_date})
            
    return render_template('search-results.html',html=div_tag)
    

@app.route('/connections',methods=['GET', 'POST'])
def connections():
    global user
    
    color_gradients = ['#a3f48f','#bbf48f','#d4f48f','#e0f48f','#f2f48f','#f4bf8f','#F48F98']
    month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
    
    try:
        box = []
        inventory = db.child(ID).get()
        for business in inventory.each():
            box += [business.val()]

        count = 0
        names = []
        emails = []
        linkedins = []
        titles = []
        dates = []
        color = []
        bar_pos = []
        div_tag = ''

        for i in box[0]:
            count += 1
            names += [i]
            emails += [box[0][i]['email']]
            linkedins += [box[0][i]['linkedin']]
            titles += [box[0][i]['title']]

            dd = box[0][i]['last-meeting'].split('-')
            month = int(dd[1])-1
            days = int(dd[2])
            for o in range(len(month_days[:month])):
                days += month_days[o]

            curr_month = int(str(datetime.datetime.now())[0:10].split('-')[1])-1
            curr_day = int(str(datetime.datetime.now())[0:10].split('-')[2])

            for w in range(len(month_days[:curr_month])):
                curr_day += month_days[w]

            time_since = curr_day-days
            dates += [time_since]

            for cc in range(7): 
                if (cc)*6 <= time_since < (cc+1)*6:
                    color += [color_gradients[cc]]

            bar_t = -80+time_since*2
            if bar_t > -10:
                bar_t = -10
            bar_pos += [bar_t]


        for i in range(count):
            div_tag += '<a href="connection-profile/{}">'.format(names[i])
            div_tag += "<div><div id='{}' class='card shadow border-left-warning py-2' style='margin-left: 0px;/*margin-right: 0%;*/height: 100px;border-left: 1px solid #e3e6f0;margin-bottom: 20px;background-color: rgb(251,251,251);/*border: 1px transparent;*/border: 1px solid transparent;border-left: .01rem solid white!important;max-width: 350px;'><div class='card-body' style='margin-top: -12px;/*border: 1px solid transparent;*/height: 100px;'><input onclick='checkBoxCheckedGood({})'".format(("connection-"+str(i+1)),str(i))
            div_tag += "type='checkbox' style='position: absolute;left: -30px;top: 42%;/*border: 1px solid black;*/background-color: black !important;filter: blur(0px) brightness(118%);font-size: 81px;width: 17px;'><div class='row align-items-center no-gutters'><div class='col' style='cursor:pointer;'><img src='assets/img/luke.png' style='width: 70px;border-radius: 50%;display: inline-block;float: left;max-height: 70px;object-fit: cover;position: relative !important;'><p style='padding-left: 10px;display: inline-block;float: left;font-family: sans-serif;font-weight: normal;padding-top: 9px;font-size: 25px;color: rgb(6,6,6);'>{}</p>".format(names[i])
            div_tag += "<p style='padding-left: 10px;display: inline-block;float: left;clear: left;margin-top: -28px;margin-left: 72px;font-size: 11px;font-family:sans-serif;font-weight: normal;color: rgb(89,89,89);'>{}</p>".format(titles[i])
            div_tag += "<p style='position: absolute;right: -135px;top: 25px;color: rgb(190,190,190);font-weight: bold;'>{}</p><a href='{}' target='blacnk'><i class='fa fa-linkedin-square' style='position: absolute;right: 0;top: 12%;font-size: 22px;color: #e2e2e2;'></i></a>".format(dates[i],linkedins[i])
            div_tag += "<a href='{}'><i class='material-icons' style='position: absolute;right: -2px;top: 54%;font-size: 22px;color: #e2e2e2;'>mail_outline</i></a></div></div><div style='position: absolute;height: 30px;width: 150px;right: -90px;top: 38%;bottom: 60%;border-radius: 15px 15px 15px 15px;background-color: white;z-index: -1;border: 2px solid #e2e2e2;'></div><div style='position: absolute;height: 30px;width: 150px;right: {}px;top: 38%;bottom: 60%;border-radius: 15px 0px 0px 15px;background-color: {};z-index: -1;border: 1px solid #e2e2e2;'></div></div></div></div></a>".format(emails[i],str(bar_pos[i]),color[i])

        if request.method == 'POST':
            try:
                user = request.form.get('search-result', None)
                return redirect(url_for('results'))
            except:
                if len(request.form.get('inside-text', None)) > 0:
                    note_content = request.form.get('inside-text', None).split("|")
                    name = note_content[0]
                    note = note_content[1]
                    loc = db.child(ID).child('connections').child(name).child('meeting').get()
                    count = 0
                    for c in loc.each():
                        count += 1
                    for j in names:
                        if j == name:
                            current_date = str(datetime.datetime.now())[0:10]
                            db.child(ID).child('connections').child(name).child('meeting').update({current_date:note})
                            db.child(ID).child('connections').child(name).update({'last-meeting':current_date})

        return render_template('professional.html',html=div_tag)

    except TypeError:
        return('404 page not found.\n\nLog in to continue.')



@app.route('/tracker',methods=['GET','POST'])
def tracker():
    global user
    
    color_gradients = ['#a3f48f','#bbf48f','#d4f48f','#e0f48f','#f2f48f','#f4bf8f','#F48F98']
    month_days = [31,28,31,30,31,30,31,31,30,31,30,31]

    box = []
    inventory = db.child(ID).get()
    for business in inventory.each():
        box += [business.val()]

    count = 0
    count_total_meeting = 0
    names = []
    emails = []
    linkedins = []
    titles = []
    dates = []
    color = []
    bar_pos = []
    meeting_dates = []
    div_tag = ''
    curr_month = int(str(datetime.datetime.now())[0:10].split('-')[1])-1
    curr_day = int(str(datetime.datetime.now())[0:10].split('-')[2])
    for w in range(len(month_days[:curr_month])):
        curr_day += month_days[w]

    day_day = ""

    for i in box[0]:
        count += 1
        names += [i]
        emails += [box[0][i]['email']]
        linkedins += [box[0][i]['linkedin']]
        titles += [box[0][i]['title']]
        dd = box[0][i]['last-meeting'].split('-')
        month = int(dd[1])-1
        days = int(dd[2])
        for o in range(len(month_days[:month])):
            days += month_days[o]
        time_since = curr_day-days
        dates += [time_since]
        for cc in range(7): 
            if (cc)*6 <= time_since < (cc+1)*6:
                color += [color_gradients[cc]]
        bar_t = -80+time_since*2
        if bar_t > -10:
            bar_t = -10
        bar_pos += [bar_t]

        for opy in box[0][i]['meeting']:
            if opy != 'none':
                full = opy.split('-')
                month_tem = int(full[1])-1
                days_tem = int(full[2])
                for owo in range(len(month_days[:month])):
                    days_tem += month_days[owo]
                count_total_meeting += 1
                meeting_dates += [days_tem]
                day_day += "cal-"+str(days_tem)+"_"
        
        day_day += "|"

    cal_lis = [i for i in range(1,366)]
    full_input = ""
    count_rps = [0]*365

    for i in range(len(cal_lis)):
        for o in meeting_dates:
            if cal_lis[i] == o:
                count_rps[i] += 1
        full_input += str(count_rps[i])+"-"
    
    prop_days = day_day.split("|")
    
    for i in range(count):
        tes = prop_days[i][0:-1]
        div_tag += '<a href="connection-profile/{}">'.format(names[i])
        div_tag += "<div id='{}' class='card shadow border-left-warning py-2' style='margin-left: 0px;/*margin-right: 0%;*/height: 100px;border-left: 1px solid #e3e6f0;margin-bottom: 20px;background-color: rgb(251,251,251);/*border: 1px transparent;*/border: 1px solid transparent;border-left: .01rem solid white!important;max-width: 350px;'><div class='card-body' style='margin-top: -12px;/*border: 1px solid transparent;*/height: 100px;'>".format(("connection-"+str(i+1)))
        div_tag += "<div class='row align-items-center no-gutters'><div class='col'><img src='assets/img/luke.png' style='width: 70px;border-radius: 50%;display: inline-block;float: left;max-height: 70px;object-fit: cover;position: relative !important;'><p style='padding-left: 10px;display: inline-block;float: left;font-family: sans-serif;font-weight: normal;padding-top: 9px;font-size: 25px;color: rgb(6,6,6);'>{}</p>".format(names[i])
        div_tag += "<p style='padding-left: 10px;display: inline-block;float: left;clear: left;margin-top: -28px;margin-left: 72px;font-size: 11px;font-family:sans-serif;font-weight: normal;color: rgb(89,89,89);'>{}</p>".format(titles[i])
        div_tag += "<p style='position: absolute;right: -135px;top: 25px;color: rgb(190,190,190);font-weight: bold;'>{}</p><a href='{}' target='blacnk'><i class='fa fa-linkedin-square' style='position: absolute;right: 0;top: 12%;font-size: 22px;color: #e2e2e2;'></i></a>".format(dates[i],linkedins[i])
        div_tag += "<a href='{}'><i class='material-icons' style='position: absolute;right: -2px;top: 54%;font-size: 22px;color: #e2e2e2;'>mail_outline</i></a></div></div><div style='position: absolute;height: 30px;width: 150px;right: -90px;top: 38%;bottom: 60%;border-radius: 15px 15px 15px 15px;background-color: white;z-index: -1;border: 2px solid #e2e2e2;'></div><div style='position: absolute;height: 30px;width: 150px;right: {}px;top: 38%;bottom: 60%;border-radius: 15px 0px 0px 15px;background-color: {};z-index: -1;border: 1px solid #e2e2e2;'></div><p style='display:none'>{}</p></div></div></a>".format(emails[i],str(bar_pos[i]),color[i],tes)

    if request.method == 'POST':
        user = request.form.get('search-result', None)
        return redirect(url_for('results'))       
        
    return render_template('tracker.html',top_statement="People you've met with",meeting_days_spec=full_input, total_meeting=count_total_meeting,html=div_tag, curr_day=curr_day-6)

# except:
#     return('404 page not found.\n\nLog in to continue.')




@app.route('/connection-profile/<name>',methods=['GET','POST'])
def connection_profile(name):
    global user
    
    try:
        month_names = ['January','Febuary','March','April','May','June','July','August','September','October','November','December']
        if request.method == 'POST':
            try:
                user = request.form.get('search-result', None)
                return redirect(url_for('results'))
            except:
                pass
            
            try:
                if request.form.get('dummy', None) == '0':
                    db.child(ID).child('connections').child(name).update({'last-meeting':str(datetime.datetime.now())[0:10]})
                    db.child(ID).child('connections').child(name).child('meeting').update({str(datetime.datetime.now())[0:10]:''}) 
            except:
                pass
            try:
                if str(request.form.get('connection-note', None)) != 'None' and len(str(request.form.get('connection-note', None))) > 0:
                    db.child(ID).child('connections').child(name).update({'note':str(request.form.get('connection-note', None))})
            except:
                pass
            try:
                if len(str(request.form.get('specific-day-note', None))) > 0:
                    month_temp_0 = str(request.form.get('specific-day-note', None)).split('-')[0].split(" ")[0]            
                    day_temp_0 = str(request.form.get('specific-day-note', None)).split('-')[0].split(" ")[1]
                    msg_temp = str(request.form.get('specific-day-note', None)).split('-')[1]

                    oo = 0
                    for i in month_names:
                        if i == month_temp_0:
                            break
                        oo+=1

                    if int(day_temp_0) < 10:
                        day_temp_0 = "0"+day_temp_0

                    in_msg = "2019-"+str(oo+1)+"-"+day_temp_0                    
                    db.child(ID).child('connections').child(name).child('meeting').update({in_msg:msg_temp})
                    db.child(ID).child('connections').child(name).update({'note':str(request.form.get('connection-note', None))})
            except:
                pass

        meeting_ind_notes = ""
        meeting_dates = []
        count_total_meeting = 0
        cal_lis = [i for i in range(1,366)]
        full_input = ""
        count_rps = [0]*365
        color_gradients = ['#a3f48f','#bbf48f','#d4f48f','#e0f48f','#f2f48f','#f4bf8f','#F48F98']
        month_days = [31,28,31,30,31,30,31,31,30,31,30,31]
        curr_month = int(str(datetime.datetime.now())[0:10].split('-')[1])-1
        curr_day = int(str(datetime.datetime.now())[0:10].split('-')[2])
        for w in range(len(month_days[:curr_month])):
            curr_day += month_days[w]

        time_since = db.child(ID).child('connections').child(name).child('last-meeting').get().val()
        old_month = int(time_since.split('-')[1])-1
        old_day = int(time_since.split('-')[2])
        for w in range(len(month_days[:old_month])):
            old_day += month_days[w]

        time_since = curr_day-old_day
        email = db.child(ID).child('connections').child(name).child('email').get().val()
        linkedin = db.child(ID).child('connections').child(name).child('linkedin').get().val()
        title = db.child(ID).child('connections').child(name).child('title').get().val()
        note = db.child(ID).child('connections').child(name).child('note').get().val()
        date_note_title = "Choose a Day"

        for opy in db.child(ID).child('connections').child(name).child('meeting').get().val():
            if opy != 'none':
                meeting_ind_notes += str(db.child(ID).child('connections').child(name).child('meeting').child(opy).get().val())+"-"
                full = opy.split('-')
                tem_month = int(opy.split('-')[1])-1
                tem_day = int(opy.split('-')[2])

                for w in range(len(month_days[:tem_month])):
                    tem_day += month_days[w]
                count_total_meeting += 1
                meeting_dates += [tem_day-5]


        date_full_titles = ""
        for i in range(8):
            date_full_titles += '00-'
        for i in range(8):
            full_input += "0-"
            
        count_rps_names = [' ']*365
        for i in range(len(cal_lis)):
            dddd = False
            for o in meeting_dates:
                if cal_lis[i] == o:
                    for jj in range(len(month_days)):
                        if o < sum(month_days[0:jj+1]):
                            ds = str(o-sum(month_days[0:jj])+5)
                            mon = month_names[jj]
                            date_full_titles += mon+" "+ds+"-"
                            dddd = True
                            break     
            if dddd == False:
                date_full_titles += '0'+'0'+"-"
                
        for i in range(len(cal_lis)):
            for o in meeting_dates:
                if cal_lis[i] == o:
                    count_rps[i] += 1
            full_input += str(count_rps[i])+"-"        

        color = ""
        for cc in range(7): 
            if (cc)*6 <= time_since < (cc+1)*6:
                color += color_gradients[cc]
            elif time_since > 30:
                color += color_gradients[-1]

        bar_t = 110-time_since*3
        if bar_t < -10:
            bar_t = -10
        bar_t = str(bar_t) + "px"        
        
#         return(str(date_note_title))
        
        return render_template('user-profile.html', name=name, title=title, meeting_days_spec=full_input, date_note_title=date_note_title, note=note, time_since=time_since, bar_width=bar_t, bar_col=color, curr_day=curr_day+2, meeting_day_titles=date_full_titles, linkedin=linkedin, meeting_ind_notes=meeting_ind_notes)
    
    except:
        return('404 page not found.\n\nLog in to continue.')









@app.route('/signup/',methods=['GET','POST'])
def signup():
    global ID
    
    if request.method == 'POST':
        firstname = request.form.get('firstname', None)
        lastname = request.form.get('lastname', None)
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        hiddenVal = request.form.get('hiddenvalue', None)
        
        box = []
        tr = False
        inventory = db.get()
        
        for business in inventory.each():
            box += [business.val()]
            
        for i in box:
            if i["email"] == email:
                tr = True
                # DO SOMETHING WHEN THE EMAIL IS USED
    
        if tr == False:
            rando = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(16)])
            ID = rando
            
            db.child(rando).update({"email":email})
            db.child(rando).update({"first-name":firstname})
            db.child(rando).update({"last-name":lastname})
            db.child(rando).update({"password":password})
            db.child(rando).update({"about":""})
            
            #storage.child(rando)
            
        if len(hiddenVal) > 1:
            return redirect(url_for('profile',username=ID))
        
    return render_template('signup.html')
















































@app.route('/messages/',methods=['GET','POST'])
def messages():
    return render_template('messages.html') 
    
    
@app.route('/todo/',methods=['GET','POST'])
def todo():
    return render_template('todo.html')



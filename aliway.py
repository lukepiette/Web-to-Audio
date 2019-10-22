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



@app.route('/',methods=['GET', 'POST'])
def index():
    return( render_template('index.html') )

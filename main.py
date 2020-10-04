from flask import Flask, escape, url_for, request, render_template, redirect, session
from flask_mysqldb import MySQL
import time
import random
import string
import hashlib
import cv2
import os
from werkzeug.utils import secure_filename
import logging
import pymysql
import pyrebase
import datetime
import html
import uuid
import gunicorn
import secrets

from requests import get
from bs4 import BeautifulSoup
import sys
from pydub import AudioSegment
import pathlib
from gtts import gTTS
import ffmpy
from tika import parser
from tempfile import TemporaryFile
from io import BytesIO
import json
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('nCHtrUHEZ7x7Jt2IdEBFWo2NFFR4wUG48z2voRo3RW98')
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
)
text_to_speech.set_service_url('https://stream.watsonplatform.net/text-to-speech/api')

config = {
    "apiKey": "AIzaSyAiS3FQF1m80-jp9-BLemrnTALqYIFidmQ",
    "authDomain": "web-to-audio.firebaseapp.com",
    "databaseURL": "https://web-to-audio.firebaseio.com",
    "projectId": "web-to-audio",
    "storageBucket": "web-to-audio.appspot.com",
    "messagingSenderId": "178178792705",
    "appId": "1:178178792705:web:36d24f1c6b30105a138f00",
    "measurementId": "G-GGCV1QY9HD"}
firebase = pyrebase.initialize_app(config)
db = firebase.database()
storage = firebase.storage()
auth = firebase.auth()
app = Flask(__name__,template_folder='templates',static_folder='static')
key = secrets.token_urlsafe(16)
app.config['SECRET_KEY'] = key
UPLOAD_FOLDER = '/tmp/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def getTextURL(URL):
    title = ""
    read_text = ""
    if URL[-4:] == ".pdf":
        try:
            raw = parser.from_file(URL)
            content = raw['content'].replace("\n", " ")
            if len(content.split("Abstract")) == 2:
                content = content.split("Abstract")[1]
            if len(content.split("REFERENCES")) == 2:
                content = content.split("REFERENCES")[0]
            elif len(content.split("References")) == 2:
                content = content.split("References")[0]
            elif len(content.split("references")) == 2:
                content = content.split("references")[0]
            read_text = content
            ft = content[0:40].split(" ")
            title = ""
            for i in range(len(ft)):
                if i == (len(ft)-1):
                    title += ft[i]
                    break
                title += ft[i]+"_"
            
        except:
            return(render_template("index.html",msg="This pdf is forbidden"))
    else:       
        response = get(URL)
        html_soup = BeautifulSoup(response.text, 'html.parser') 
        ### Title ###
        title = html_soup.find("title")
        ft = title.get_text().split(" ")
        file_title = ""
        for i in range(len(ft)):
            if i == (len(ft)-1):
                file_title += ft[i]
                break
            file_title += ft[i]+"_"
        ### Text ###
        text = html_soup.find_all('p')
        read_text = ""
        for i in text:
            read_text += i.get_text()
        read_text = read_text.split("\xa0")
        x = lambda x: " ".join(x)
        read_text = x(read_text).replace("\n", " ")
        
        read_text = read_text.split(".")
        read_t = ""
        for i in read_text:
            if i[0:2] == "  ":
                read_t += i[1:]
                read_t += "."
            elif i[0:1] == " ":
                read_t += i
                read_t += "."
            else:
                j = " "+i+"."
                read_t += j
        read_text = read_t
        title = file_title
    return(read_text,title)

def getTextCTRLV(URL):
    ft = URL[0:40].split(" ")
    title = ""
    for i in range(len(ft)):
        if i == (len(ft)-1):
            title += ft[i]
            break
        title += ft[i]+"_"
    return(URL,title)

def getFullText(URL):
    if URL[0:8] == 'https://'or URL[0:7] == 'http://':
        read_text,title = getTextURL(URL)
        return(textToSpeech(read_text,title))
    else:
        read_text,title = getTextCTRLV(URL)
        return(textToSpeech(read_text,title))

def textToSpeech(read_text,title):
    src = title+".mp3"
    src_x = title+"[1.3x].mp3"
    voice_list = ['en-US_MichaelV3Voice','en-US_AllisonV3Voice']
    div_num = 4900
    num = int(len(read_text)/div_num)
    base = []
    
    for i in range(num+1):
        with open(app.config['UPLOAD_FOLDER']+'{}.mp3'.format(title+str(i)), 'wb') as audio_file:
            audio_file.write(
                text_to_speech.synthesize(
                    read_text[i*div_num:(i+1)*div_num],
                    voice=voice_list[0],
                    accept='audio/mp3'        
                ).get_result().content)
        with open(app.config['UPLOAD_FOLDER']+'{}.mp3'.format(title+str(i)), 'rb') as www:
            base += [www.read()]
            
    bg = base[0]
    for i in range(len(base)-1):
        bg += base[i+1]
    with open(app.config['UPLOAD_FOLDER']+src,"wb") as w:
        w.write(bg)

    ff = ffmpy.FFmpeg(inputs={app.config['UPLOAD_FOLDER']+src: None}, outputs={app.config['UPLOAD_FOLDER']+src_x: ["-filter:a", "atempo=1.3"]})
    ff.run()

    storage.child("audio/"+src_x).put(app.config['UPLOAD_FOLDER']+src_x)
    audio_play = storage.child("audio/"+src_x).get_url(src_x)

    return(audio_play,title)
    
    
# @app.route('/test',methods=['GET', 'POST'])
# def tester():
#     read_text = "what's up dog I've been missing you!"
#     title = "yoo_sup_dog"
    
    
    
@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        URL = request.form.get('url',None)
        audio_play,title = getFullText(URL)
        return(render_template("index.html",audio_play=audio_play))

    return(render_template("index.html"))

@app.route('/<validID>',methods=['GET', 'POST'])
def index_log(validID):
    if request.method == 'POST':
        for jjj in range(5):
            try:
                URL = request.form.get('url',None)
                audio_play,title = getFullText(URL)
                db.child(validID).child("downloads").update({str(uuid.uuid1()):{"title":title,"url":audio_play}})
                return(render_template("index.html",audio_play=audio_play,validID=validID))
            except:
                time.sleep(0.2)
    return(render_template("index.html",validID=validID))


@app.route('/fork',methods=['GET', 'POST'])
def fork():
    return(render_template("fork.html"))


@app.route('/downloads/<validID>',methods=['GET', 'POST'])
def downloads(validID):
    box = []
    inventory = db.child(validID).get()
    for business in inventory.each():
        box += [business.val()]

    final_string = ""

    try:
        for w in range(len(box[0])):
            jj = list(box[0])[w]
            title = box[0][jj]['title'][0:50]
            url = box[0][jj]['url']

            temp_len = int(len(title)/40)
            titl = title.split("_")
            title = ""
            for i in titl:
                title+=i
                title+=" "
            if len(title) > 40:
                title = title[0:40]+"..."

            audid = "audio-"+str(w)
            final_string += "<div><button class='btn btn-primary' type='button' style='font-family: Staatliches, cursive;color: rgb(255,255,255);background-color: transparent !important;border: none;text-shadow: -3px 3px 1px rgba(61,193,145,.5);padding-top: 0px;padding-bottom: 0px;padding-left: 2px;padding-right: 2px;margin-right: 10px !important;text-align: left;min-width:400px !important;margin-left: auto;margin-right: auto;display: inline-block;'>{}<i onclick='deleteAudio(event)' id='{}' class='fa fa-close' style='color:white;margin-left:1%;text-align:right;display:inline-block !important;z-index:10 !important'></i></button><div><audio controls='' style='margin-top: 2%;margin-bottom: 4%;'><source src='{}' type='audio/mpeg'></audio></div></div>".format(title,audid,url)

    except:
        pass

    if request.method == 'POST':
        text_ = request.form.get('text',None)
        num = int(text_.split("-")[1])
        jj = str(list(box[0])[num])
        db.child(validID).child('downloads').child(jj).remove()

    return(render_template("downloads.html",validID=validID,download_files=final_string))

    
    
@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form.get('email', None)
            password = request.form.get('password', None)

            user_cred = auth.sign_in_with_email_and_password(email,password)
            ID = auth.get_account_info(user_cred['idToken'])['users'][0]['localId']
            
            if not auth.get_account_info(user_cred['idToken'])['users'][0]['emailVerified']:
                return redirect(url_for('email_verify',validID=ID))
            
            for i in range(5):
                try:
                    return redirect(url_for('downloads',validID=ID))
                except:
                    time.sleep(0.2)
        except:
            return redirect(url_for('login'))
        
    return(render_template("login.html"))


@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email',None)
        password = request.form.get('password',None)
        
        try:
            user_cred = auth.create_user_with_email_and_password(email,password)
            ID = user_cred['localId']
            db.child(ID).update({"p":"p"})
            return redirect(url_for('email_verify',validID=user_cred['idToken']))
        except:
            return render_template('signup.html')
           
    return(render_template("signup.html"))


@app.route('/email_verify/<validID>',methods=['GET', 'POST'])
def email_verify(validID):
    try:
        auth.send_email_verification(validID)
    except:
        pass
    return render_template('email_verify.html',validID=validID)


if __name__ == '__main__':
    app.run(debug=True)


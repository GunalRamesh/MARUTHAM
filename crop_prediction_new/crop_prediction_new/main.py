# main.py
import os
import base64
import io
import math
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import mysql.connector
import hashlib
import datetime
import calendar
import random
from random import randint
from urllib.request import urlopen
import webbrowser
#from plotly import graph_objects as go

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import urllib.request
import urllib.parse
import csv
import seaborn as sns

import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

from sklearn.model_selection import train_test_split
import lightgbm as lgb
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="crop"

)
app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#######
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = { 'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#####
@app.route('/', methods=['GET', 'POST'])
def index():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM register WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('userhome'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('index.html',msg=msg)








@app.route('/ask_ques',methods=['POST','GET'])
def ask_ques():
    if 'username' not in session or session.get('user_type') != 'farmer':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('login_user'))

    
    username=session.get('username')

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM questions where username = %s",(username,))
    data3 = cursor.fetchall()
    cursor.close()
    
    msg=""
    if request.method=='POST':
        question=request.form['question']
        
        now = datetime.datetime.now()
        reg_date=now.strftime("%Y-%m-%d")
        
        mycursor = mydb.cursor()
        
        mycursor.execute("SELECT max(id)+1 FROM questions")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO questions(id, question, reg_date, username) VALUES (%s, %s, %s, %s)"
        val = (maxid, question, reg_date, username)
        mycursor.execute(sql, val)
        mydb.commit()

        msg="success"


    
  
    return render_template('ask_ques.html', msg=msg, questions=data3)


@app.route('/view_sugg',methods=['POST','GET'])
def view_sugg():
    if 'username' not in session or session.get('user_type') != 'farmer':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('login_user'))

    
    sid=request.args.get('sid')

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM suggestion where qid=%s",(sid, ))
    data3 = cursor.fetchall()
    cursor.close()
    
  
    return render_template('view_sugg.html', suggestion=data3)





@app.route('/write',methods=['POST','GET'])
def write():
    if 'username' not in session or session.get('user_type') != 'farmer':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('login_user'))

    
    username=session.get('username')

    qid=request.args.get("qid")
    
    msg=""
    if request.method=='POST':
        sugges=request.form['sugges']
        
        now = datetime.datetime.now()
        reg_date=now.strftime("%Y-%m-%d")
        
        mycursor = mydb.cursor()
        
        mycursor.execute("SELECT max(id)+1 FROM suggestion")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
        sql = "INSERT INTO suggestion(id, qid, reg_date, sugges, username) VALUES (%s, %s, %s, %s, %s)"
        val = (maxid, qid, reg_date, sugges, username)
        mycursor.execute(sql, val)
        mydb.commit()

        msg="success"
    
  
    return render_template('write.html', msg=msg)


@app.route('/sugg',methods=['POST','GET'])
def sugg():
    if 'username' not in session or session.get('user_type') != 'farmer':
        print("Please log in as a admin to access the page.", 'danger')
        return redirect(url_for('login_user'))

    
    username=session.get('username')

    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM questions")
    data3 = cursor.fetchall()
    cursor.close()
    
  
    return render_template('sugg.html', questions=data3)










@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)

@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    msg=""

    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM register WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            session['user_type'] = 'farmer'
            return redirect(url_for('userhome'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_user.html',msg=msg)


@app.route('/register', methods=['GET', 'POST'])
def register():
    #import student
    msg=""
    if request.method=='POST':
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        uname=request.form['uname']
        pass1=request.form['pass']
        
        
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM register where uname=%s",(uname,))
        cnt = mycursor.fetchone()[0]

        if cnt==0:
            mycursor.execute("SELECT max(id)+1 FROM register")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1
                    
            sql = "INSERT INTO register(id,name,mobile,email,uname,pass) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (maxid,name,mobile,email,uname,pass1)
            mycursor.execute(sql, val)
            mydb.commit()            
            #print(mycursor.rowcount, "Registered Success")
            msg="success"
            
        else:
            msg='Already Exist'
    return render_template('register.html',msg=msg)

@app.route('/add_fert', methods=['GET', 'POST'])
def add_fert():
    msg=""
    mycursor = mydb.cursor()

    dv = pd.read_csv('dataset/Crop_recommendation.csv')
    dtt=[]
    for dd in dv.values:
        dtt.append(dd[7])
    crop2=unique(dtt)

    
    if request.method=='POST':
        crop=request.form['crop']
        fert=request.form['fert']
        pest=request.form['pest']
        
        

        mycursor.execute("SELECT max(id)+1 FROM fert_data")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1
                
        sql = "INSERT INTO fert_data(id,crop,fert,pest) VALUES (%s, %s, %s, %s)"
        val = (maxid,crop,fert,pest)
        mycursor.execute(sql, val)
        mydb.commit()            
        #print(mycursor.rowcount, "Registered Success")
        msg="success"
        return redirect(url_for('add_fert'))
        
    mycursor.execute("SELECT * FROM fert_data")
    data = mycursor.fetchall()

    
    return render_template('add_fert.html',msg=msg,data=data,crop2=crop2)

def unique(list1):
 
    # initialize a null list
    unique_list = []
 
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x not in unique_list:
            unique_list.append(x)
    # print list
    #for x in unique_list:
    #    print x,
    return unique_list

@app.route('/user_sample', methods=['GET', 'POST'])
def user_sample():
    msg=""
    cnt=0
    crop=[]
    st=""
    st2=""
    crop2=[]
    data=[]
    result=""
    uname=""
    act = request.args.get('act')
    cat = request.args.get('cat')
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM register where uname=%s",(uname,))
    usr = mycursor.fetchone()

    dv = pd.read_csv('dataset/Crop_recommendation.csv')
    dv2 = pd.read_csv('dataset/fertilizer.csv')
    x=0

    ff=open("static/crops.txt","r")
    crop1=ff.read()
    ff.close()
    if len(crop1)>0:
        crop2=crop1.split(',')

                
    if request.method=='POST':
        if act=="1":
            v1=request.form['v1']
            v2=request.form['v2']
            v3=request.form['v3']
            temp=request.form['temp']
            hu=request.form['humidity']
            ph=request.form['ph']
            rain=request.form['rainfall']

       
            v11=float(v1)
            v22=float(v2)
            v33=float(v3)
            t11=float(temp)
            h11=float(hu)
            p11=float(ph)
            r11=float(rain)

            n1=v11-15
            n2=v11+15

            p1=v22-15
            p2=v22+15

            k1=v33-15
            k2=v33+15

            t1=t11-15
            t2=t11+15

            h1=h11-15
            h2=h11+15

            dt=[]
            for dd in dv2.values:
                if n1<=v11 and n2>=v11 and p1<=v22 and p2>=v22 and k1<=v33 and k2>=v33 and t1<=t11 and t2>=t11 and h1<=h11 and h2>=h11:
                    dt.append(dd[4])
                
            ncrop=len(dt)
            if ncrop>0:
                crop=unique(dt)
                cc=','.join(crop)
                ff=open("static/crops.txt","w")
                ff.write(cc)
                ff.close()
                st="1"
            else:
                st="2"

            ####
        elif act=="2":
            cnt=0
            s1="1"
            crop3=request.form['crop3']
            dt=[]
            for dd in dv2.values:
                if dd[4]==crop3:
                    cnt+=1
                    dtt=[]
                    dtt.append(dd[3])
                    dtt.append(dd[8])
                    data.append(dtt)
            if cnt>0:
                result="1"
            else:
                result="2"
    
    return render_template('user_sample.html',msg=msg,usr=usr,st=st,result=result,crop2=crop2,data=data,st2=st2)

def getValue(arr):
    #arr = [10, 89, 9, 56, 4, 80, 8]
    mini = arr[0]
    maxi = arr[0]

    for i in range(len(arr)):
      if arr[i] < mini: mini = arr[i] 
      
    if arr[i] > maxi: maxi = arr[i]

    #print (mini)
    #print (maxi)
    mini1=round(mini,2)
    maxi1=round(maxi,2)
    v=[mini1,maxi1]
    return v


    
@app.route('/userhome1', methods=['GET', 'POST'])
def userhome1():
    msg=""
    cnt=0
    crop=[]
    s1=""
    st2=""
    crop1=""
    crop2=[]
    data2=[]
    data=[]
    result=""
    uname=""
    act = request.args.get('act')
    cat = request.args.get('cat')
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM register where uname=%s",(uname,))
    usr = mycursor.fetchone()

    dv = pd.read_csv('dataset/Crop_recommendation.csv')
    dtt=[]
    for dd in dv.values:
        dtt.append(dd[7])
    crop2=unique(dtt)
    
                
    if request.method=='POST':        
        crop=request.form['crop']
        crop1=crop
        s1="1"
        a_n=[]
        a_p=[]
        a_k=[]
        a_t=[]
        a_h=[]
        a_ph=[]
        a_r=[]
        for dd in dv.values:
            if dd[7]==crop:
                a_n.append(int(dd[0]))
                a_p.append(int(dd[1]))
                a_k.append(int(dd[2]))
                a_t.append(float(dd[3]))
                a_h.append(float(dd[4]))
                a_ph.append(float(dd[5]))
                a_r.append(float(dd[6]))
                
        n_m=getValue(a_n)
        n_min=n_m[0]
        n_max=n_m[1]

        p_m=getValue(a_p)
        p_min=p_m[0]
        p_max=p_m[1]

        k_m=getValue(a_k)
        k_min=k_m[0]
        k_max=k_m[1]

        t_m=getValue(a_t)
        t_min=t_m[0]
        t_max=t_m[1]

        h_m=getValue(a_h)
        h_min=h_m[0]
        h_max=h_m[1]

        ph_m=getValue(a_ph)
        ph_min=ph_m[0]
        ph_max=ph_m[1]

        r_m=getValue(a_r)
        r_min=r_m[0]
        r_max=r_m[1]
        data=[n_min,n_max,p_min,p_max,k_min,k_max,t_min,t_max,h_min,h_max,ph_min,ph_max,r_min,r_max]

        mycursor.execute("SELECT count(*) FROM fert_data where crop=%s",(crop,))
        nn = mycursor.fetchone()[0]
        if nn>0:
            st2="1"
            mycursor.execute("SELECT * FROM fert_data where crop=%s",(crop,))
            data2 = mycursor.fetchall()
    


    return render_template('userhome1.html',msg=msg,usr=usr,s1=s1,result=result,crop2=crop2,data=data,st2=st2,data2=data2,crop1=crop1)


@app.route('/userhome', methods=['GET', 'POST'])
def userhome():
    msg=""
    cnt=0
    crop=""
    price=""
    st=""
    st2=""
    data=""
    result=""
    uname=""
    act = request.args.get('act')
    cat = request.args.get('cat')
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM register where uname=%s",(uname,))
    usr = mycursor.fetchone()


    x=0
    if request.method=='POST':
        v1=request.form['v1']
        v2=request.form['v2']
        v3=request.form['v3']
        temp=request.form['temp']
        hu=request.form['humidity']
        ph=request.form['ph']
        rain=request.form['rainfall']

   
        v11=float(v1)
        v22=float(v2)
        v33=float(v3)
        t1=float(temp)
        h1=float(hu)
        p1=float(ph)
        r1=float(rain)
            
        dv = pd.read_csv('dataset/Crop_recommendation.csv')
        
        data2=[]
        
        act="1"

        if v11<0 or v11>140:
            x+=1
        if v22<5 or v22>145:
            x+=1
        if v33<5 or v33>205:
            x+=1
        if t1<8 or t1>43:
            x+=1
        if h1<14 or h1>99:
            x+=1
        if p1<3 or p1>9:
            x+=1
        if r1<20 or r1>298:
            x+=1
            
        if x==0:
            st="1"
            for ss2 in dv.values:
                
                g1=v11-8
                g2=v11+8
                
                g11=v22-8
                g12=v22+8

                g21=v33-8
                g22=v33+8

                tt1=t1-8
                tt2=t1+8

                hh1=h1-8
                hh2=h1+8

                pp1=p1-8
                pp2=p1+8

                rr1=r1-8
                rr2=r1+8
                
                if ss2[0]>=g1 and ss2[0]<=g2 and ss2[1]>=g11 and ss2[1]<=g12 and ss2[2]>=g21 and ss2[2]<=g22:
                    if ss2[3]>=tt1 and ss2[3]<=tt2 and ss2[4]>=hh1 and ss2[4]<=hh2 and ss2[5]>=pp1 and ss2[5]<=pp2 and ss2[6]>=rr1 and ss2[6]<=rr2:
                
                        result="1"
                        crop=ss2[7]
                        price=ss2[8]
                        

                        mycursor.execute("SELECT count(*) FROM fert_data where crop=%s",(crop,))
                        cc = mycursor.fetchone()[0]
                        if cc>0:
                            st2="1"

                            mycursor.execute("SELECT * FROM fert_data where crop=%s",(crop,))
                            data = mycursor.fetchone()
                        print("aa")
                        break
                    else:
                        if (ss2[0]>=g1 and ss2[0]<=g2):
                            result="1"
                            crop=ss2[7]
                            price=ss2[8]

                            mycursor.execute("SELECT count(*) FROM fert_data where crop=%s",(crop,))
                            cc = mycursor.fetchone()[0]
                            if cc>0:
                                st2="1"

                                mycursor.execute("SELECT * FROM fert_data where crop=%s",(crop,))
                                data = mycursor.fetchone()
                            print("bb")
                            break
                        
                    
                else:
                    if (ss2[0]>=g1 and ss2[0]<=g2):
                        result="1"
                        crop=ss2[7]
                        price=ss2[8]
                        print(ss2[0])
                        print(crop)
                        print(g1)
                        print(g2)

                        mycursor.execute("SELECT count(*) FROM fert_data where crop=%s",(crop,))
                        cc = mycursor.fetchone()[0]
                        if cc>0:
                            st2="1"

                            mycursor.execute("SELECT * FROM fert_data where crop=%s",(crop,))
                            data = mycursor.fetchone()
                        print("cc")
                        break
                    else:
                        
                        result="2"
        else:
            st="2"

        ####
        
    
    return render_template('userhome.html',msg=msg,usr=usr,st=st,result=result,crop=crop,data=data,st2=st2, price=price)




@app.route('/admin', methods=['GET', 'POST'])
def admin():
    msg=""

    x = os.listdir("./dataset")
    #print(x)
    
    if request.method=='POST':
        return redirect(url_for('process1'))
        
    return render_template('admin.html',msg=msg,dfile=x)

@app.route('/process1', methods=['GET', 'POST'])
def process1():
    msg=""
    colorarr = ['#0592D0','#Cd7f32', '#E97451', '#Bdb76b', '#954535', '#C2b280', '#808000','#C2b280', '#E4d008', '#9acd32', '#Eedc82', '#E4d96f',
           '#32cd32','#39ff14','#00ff7f', '#008080', '#36454f', '#F88379', '#Ff4500', '#Ffb347', '#A94064', '#E75480', '#Ffb6c1', '#E5e4e2',
           '#Faf0e6', '#8c92ac', '#Dbd7d2','#A7a6ba', '#B38b6d']
    
    '''data1=[]
    i=0
    sd=len(homepage)
    rows=len(homepage.values)
    for ss in homepage.values:
        cnt=len(ss)
        data1.append(ss)
    cols=cnt
    #print(data1)'
    ##################
    data2=[]
    for ss2 in payment.values:
        data2.append(ss2)'''
    ##################
    cropdf = pd.read_csv("dataset/Crop_recommendation.csv")
    dat=cropdf.head()
    data=[]
    for ss in dat.values:
        data.append(ss)

    data2=cropdf.shape
    data3=cropdf.columns
    data4=cropdf.isnull().any()

    ##print("Number of various crops: ", len(cropdf['label'].unique()))
    ##print("List of crops: ", cropdf['label'].unique())

    dat3=cropdf['label'].value_counts()
    data5=[]
    ##for ss5 in dat5.values:
    ##    data5.append(ss5)
    ##print(dat5)

    dat1=len(cropdf['label'].unique())
    dat2=cropdf['label'].unique()
    i=0
    dd=[]
    while i<dat1:
        dd.append(dat2[i])
        dd.append(dat3[i])
        data5.append(dd)
        i+=1

    crop_summary = pd.pivot_table(cropdf,index=['label'],aggfunc='mean')
    dat5=crop_summary.head()
    data5=[]
    for ss5 in dat5.values:
        data5.append(ss5)
    
    return render_template('process1.html',data=data,data2=data2,data3=data3,data4=data4,data5=data5)

@app.route('/process2', methods=['GET', 'POST'])
def process2():
    msg=""
    colorarr = ['#0592D0','#Cd7f32', '#E97451', '#Bdb76b', '#954535', '#C2b280', '#808000','#C2b280', '#E4d008', '#9acd32', '#Eedc82', '#E4d96f',
           '#32cd32','#39ff14','#00ff7f', '#008080', '#36454f', '#F88379', '#Ff4500', '#Ffb347', '#A94064', '#E75480', '#Ffb6c1', '#E5e4e2',
           '#Faf0e6', '#8c92ac', '#Dbd7d2','#A7a6ba', '#B38b6d']
    
    '''data1=[]
    i=0
    sd=len(homepage)
    rows=len(homepage.values)
    for ss in homepage.values:
        cnt=len(ss)
        data1.append(ss)
    cols=cnt
    #print(data1)'
    ##################
    data2=[]
    for ss2 in payment.values:
        data2.append(ss2)'''
    ##################
    cropdf = pd.read_csv("dataset/Crop_recommendation.csv")
    dat=cropdf.head()
    data=[]
    for ss in dat.values:
        data.append(ss)

    data2=cropdf.shape
    data3=cropdf.columns
    data4=cropdf.isnull().any()

    ##print("Number of various crops: ", len(cropdf['label'].unique()))
    ##print("List of crops: ", cropdf['label'].unique())

    dat3=cropdf['label'].value_counts()
    data5=[]
    ##for ss5 in dat5.values:
    ##    data5.append(ss5)
    ##print(dat5)

    dat1=len(cropdf['label'].unique())
    dat2=cropdf['label'].unique()
    i=0
    dd=[]
    while i<dat1:
        dd.append(dat2[i])
        dd.append(dat3[i])
        data5.append(dd)
        i+=1

    crop_summary = pd.pivot_table(cropdf,index=['label'],aggfunc='mean')
    dat5=crop_summary.head()
    data5=[]
    for ss5 in dat5.values:
        data5.append(ss5)
    #####
    ##Nitrogen Analysis
    '''crop_summary_N = crop_summary.sort_values(by='N', ascending=False)
  
    fig = make_subplots(rows=1, cols=2)

    top = {
        'y' : crop_summary_N['N'][0:10].sort_values().index,
        'x' : crop_summary_N['N'][0:10].sort_values()
    }

    last = {
        'y' : crop_summary_N['N'][-10:].index,
        'x' : crop_summary_N['N'][-10:]
    }

    fig.add_trace(
        go.Bar(top,
               name="Most nitrogen required",
               marker_color=random.choice(colorarr),
               orientation='h',
              text=top['x']),
        
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(last,
               name="Least nitrogen required",
               marker_color=random.choice(colorarr),
               orientation='h',
              text=last['x']),
        row=1, col=2
    )
    fig.update_traces(texttemplate='%{text}', textposition='inside')
    fig.update_layout(title_text="Nitrogen (N)",
                      plot_bgcolor='white',
                      font_size=12, 
                      font_color='black',
                     height=500)

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)'''
    ##fig.show()
    ##graph1
    ##############################
    ##Phosphorus Analysis
    '''crop_summary_P = crop_summary.sort_values(by='P', ascending=False)
  
    fig = make_subplots(rows=1, cols=2)

    top = {
        'y' : crop_summary_P['P'][0:10].sort_values().index,
        'x' : crop_summary_P['P'][0:10].sort_values()
    }

    last = {
        'y' : crop_summary_P['P'][-10:].index,
        'x' : crop_summary_P['P'][-10:]
    }

    fig.add_trace(
        go.Bar(top,
               name="Most phosphorus required",
               marker_color=random.choice(colorarr),
               orientation='h',
              text=top['x']),
        
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(last,
               name="Least phosphorus required",
               marker_color=random.choice(colorarr),
               orientation='h',
              text=last['x']),
        row=1, col=2
    )
    fig.update_traces(texttemplate='%{text}', textposition='inside')
    fig.update_layout(title_text="Phosphorus (P)",
                      plot_bgcolor='white',
                      font_size=12, 
                      font_color='black',
                     height=500)

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)'''
    ##fig.show()
    ##graph2
    #######################
    ##Potassium analysis
    '''crop_summary_K = crop_summary.sort_values(by='K', ascending=False)
  
    fig = make_subplots(rows=1, cols=2)

    top = {
        'y' : crop_summary_K['K'][0:10].sort_values().index,
        'x' : crop_summary_K['K'][0:10].sort_values()
    }

    last = {
        'y' : crop_summary_K['K'][-10:].index,
        'x' : crop_summary_K['K'][-10:]
    }

    fig.add_trace(
        go.Bar(top,
               name="Most potassium required",
               marker_color=random.choice(colorarr),
               orientation='h',
              text=top['x']),
        
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(last,
               name="Least potassium required",
               marker_color=random.choice(colorarr),
               orientation='h',
              text=last['x']),
        row=1, col=2
    )
    fig.update_traces(texttemplate='%{text}', textposition='inside')
    fig.update_layout(title_text="Potassium (K)",
                      plot_bgcolor='white',
                      font_size=12, 
                      font_color='black',
                     height=500)

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)'''
    ##fig.show()
    ##graph3
    #########################
    ##N, P, K values comparision between crops
    '''fig = go.Figure()
    fig.add_trace(go.Bar(
        x=crop_summary.index,
        y=crop_summary['N'],
        name='Nitrogen',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=crop_summary.index,
        y=crop_summary['P'],
        name='Phosphorous',
        marker_color='lightsalmon'
    ))
    fig.add_trace(go.Bar(
        x=crop_summary.index,
        y=crop_summary['K'],
        name='Potash',
        marker_color='crimson'
    ))

    fig.update_layout(title="N, P, K values comparision between crops",
                      plot_bgcolor='white',
                      barmode='group',
                      xaxis_tickangle=-45)'''

    ##fig.show()
    ##graph4
    #####################
    ##NPK ratio for rice, cotton, jute, maize, lentil
    labels = ['Nitrogen(N)','Phosphorous(P)','Potash(K)']
    fig = make_subplots(rows=1, cols=5, specs=[[{'type':'domain'}, {'type':'domain'},
                                                {'type':'domain'}, {'type':'domain'}, 
                                                {'type':'domain'}]])

    rice_npk = crop_summary[crop_summary.index=='rice']
    values = [rice_npk['N'][0], rice_npk['P'][0], rice_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Rice"),1, 1)

    cotton_npk = crop_summary[crop_summary.index=='cotton']
    values = [cotton_npk['N'][0], cotton_npk['P'][0], cotton_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Cotton"),1, 2)

    jute_npk = crop_summary[crop_summary.index=='jute']
    values = [jute_npk['N'][0], jute_npk['P'][0], jute_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Jute"),1, 3)

    maize_npk = crop_summary[crop_summary.index=='maize']
    values = [maize_npk['N'][0], maize_npk['P'][0], maize_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Maize"),1, 4)

    lentil_npk = crop_summary[crop_summary.index=='lentil']
    values = [lentil_npk['N'][0], lentil_npk['P'][0], lentil_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Lentil"),1, 5)

    '''fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    fig.update_layout(
        title_text="NPK ratio for rice, cotton, jute, maize, lentil",
        annotations=[dict(text='Rice',x=0.06,y=0.8, font_size=15, showarrow=False),
                     dict(text='Cotton',x=0.26,y=0.8, font_size=15, showarrow=False),
                     dict(text='Jute',x=0.50,y=0.8, font_size=15, showarrow=False),
                     dict(text='Maize',x=0.74,y=0.8, font_size=15, showarrow=False),
                    dict(text='Lentil',x=0.94,y=0.8, font_size=15, showarrow=False)])'''
    #fig.show()
    #graph5
    #############
    ##NPK ratio for fruits
    labels = ['Nitrogen(N)','Phosphorous(P)','Potash(K)']
    specs = [[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}],[
             {'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}]]
    fig = make_subplots(rows=2, cols=5, specs=specs)
    cafe_colors =  ['rgb(255, 128, 0)', 'rgb(0, 153, 204)', 'rgb(173, 173, 133)']

    apple_npk = crop_summary[crop_summary.index=='apple']
    values = [apple_npk['N'][0], apple_npk['P'][0], apple_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Apple", marker_colors=cafe_colors),1, 1)

    banana_npk = crop_summary[crop_summary.index=='banana']
    values = [banana_npk['N'][0], banana_npk['P'][0], banana_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Banana", marker_colors=cafe_colors),1, 2)

    grapes_npk = crop_summary[crop_summary.index=='grapes']
    values = [grapes_npk['N'][0], grapes_npk['P'][0], grapes_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Grapes", marker_colors=cafe_colors),1, 3)

    orange_npk = crop_summary[crop_summary.index=='orange']
    values = [orange_npk['N'][0], orange_npk['P'][0], orange_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Orange", marker_colors=cafe_colors),1, 4)

    mango_npk = crop_summary[crop_summary.index=='mango']
    values = [mango_npk['N'][0], mango_npk['P'][0], mango_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Mango", marker_colors=cafe_colors),1, 5)

    coconut_npk = crop_summary[crop_summary.index=='coconut']
    values = [coconut_npk['N'][0], coconut_npk['P'][0], coconut_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Coconut", marker_colors=cafe_colors),2, 1)

    papaya_npk = crop_summary[crop_summary.index=='papaya']
    values = [papaya_npk['N'][0], papaya_npk['P'][0], papaya_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Papaya", marker_colors=cafe_colors),2, 2)

    pomegranate_npk = crop_summary[crop_summary.index=='pomegranate']
    values = [pomegranate_npk['N'][0], pomegranate_npk['P'][0], pomegranate_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Pomegranate", marker_colors=cafe_colors),2, 3)

    watermelon_npk = crop_summary[crop_summary.index=='watermelon']
    values = [watermelon_npk['N'][0], watermelon_npk['P'][0], watermelon_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Watermelon", marker_colors=cafe_colors),2, 4)

    muskmelon_npk = crop_summary[crop_summary.index=='muskmelon']
    values = [muskmelon_npk['N'][0], muskmelon_npk['P'][0], muskmelon_npk['K'][0]]
    '''fig.add_trace(go.Pie(labels=labels, values=values,name="Muskmelon", marker_colors=cafe_colors),2, 5)

    fig.update_layout(
        title_text="NPK ratio for fruits",
        annotations=[dict(text='Apple',x=0.06,y=1.08, font_size=15, showarrow=False),
                     dict(text='Banana',x=0.26,y=1.08, font_size=15, showarrow=False),
                     dict(text='Grapes',x=0.50,y=1.08, font_size=15, showarrow=False),
                     dict(text='Orange',x=0.74,y=1.08, font_size=15, showarrow=False),
                    dict(text='Mango',x=0.94,y=1.08, font_size=15, showarrow=False),
                    dict(text='Coconut',x=0.06,y=0.46, font_size=15, showarrow=False),
                     dict(text='Papaya',x=0.26,y=0.46, font_size=15, showarrow=False),
                     dict(text='Pomegranate',x=0.50,y=0.46, font_size=15, showarrow=False),
                     dict(text='Watermelon',x=0.74,y=0.46, font_size=15, showarrow=False),
                    dict(text='Muskmelon',x=0.94,y=0.46, font_size=15, showarrow=False)])'''
    #fig.show()
    #graph6
    ##############
    crop_scatter = cropdf[(cropdf['label']=='rice') | 
                      (cropdf['label']=='jute') | 
                      (cropdf['label']=='cotton') |
                     (cropdf['label']=='maize') |
                     (cropdf['label']=='lentil')]

    fig = px.scatter(crop_scatter, x="temperature", y="humidity", color="label", symbol="label")
    fig.update_layout(plot_bgcolor='white')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)

    #fig.show()
    #graph7
    ###################
    '''fig = px.bar(crop_summary, x=crop_summary.index, y=["rainfall", "temperature", "humidity"])
    fig.update_layout(title_text="Comparision between rainfall, temerature and humidity",
                      plot_bgcolor='white',
                     height=500)

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)'''
    #fig.show()
    #graph8
    ####################
    ##Correlation between different features
    fig, ax = plt.subplots(1, 1, figsize=(15, 9))
    sns.heatmap(cropdf.corr(), annot=True,cmap='Wistia' )
    ax.set(xlabel='features')
    ax.set(ylabel='features')

    #plt.title('Correlation between different features', fontsize = 15, c='black')
    #plt.show()
    #graph9
    ###################

    
    return render_template('process2.html')

@app.route('/process3', methods=['GET', 'POST'])
def process3():
    msg=""
    colorarr = ['#0592D0','#Cd7f32', '#E97451', '#Bdb76b', '#954535', '#C2b280', '#808000','#C2b280', '#E4d008', '#9acd32', '#Eedc82', '#E4d96f',
           '#32cd32','#39ff14','#00ff7f', '#008080', '#36454f', '#F88379', '#Ff4500', '#Ffb347', '#A94064', '#E75480', '#Ffb6c1', '#E5e4e2',
           '#Faf0e6', '#8c92ac', '#Dbd7d2','#A7a6ba', '#B38b6d']
    
    '''data1=[]
    i=0
    sd=len(homepage)
    rows=len(homepage.values)
    for ss in homepage.values:
        cnt=len(ss)
        data1.append(ss)
    cols=cnt
    #print(data1)'
    ##################
    data2=[]
    for ss2 in payment.values:
        data2.append(ss2)'''
    ##################
    cropdf = pd.read_csv("dataset/Crop_recommendation.csv")
    dat=cropdf.head()
    data=[]
    for ss in dat.values:
        data.append(ss)

    data2=cropdf.shape
    data3=cropdf.columns
    data4=cropdf.isnull().any()

    #print("Number of various crops: ", len(cropdf['label'].unique()))
    #print("List of crops: ", cropdf['label'].unique())

    dat3=cropdf['label'].value_counts()
    data5=[]
    #for ss5 in dat5.values:
    #    data5.append(ss5)
    #print(dat5)

    dat1=len(cropdf['label'].unique())
    dat2=cropdf['label'].unique()
    i=0
    dd=[]
    while i<dat1:
        dd.append(dat2[i])
        dd.append(dat3[i])
        data5.append(dd)
        i+=1

    crop_summary = pd.pivot_table(cropdf,index=['label'],aggfunc='mean')
    dat5=crop_summary.head()
    data5=[]
    for ss5 in dat5.values:
        data5.append(ss5)
    #####
    ##Nitrogen Analysis
    '''crop_summary_N = crop_summary.sort_values(by='N', ascending=False)
  
    fig = make_subplots(rows=1, cols=2)

    top = {
        'y' : crop_summary_N['N'][0:10].sort_values().index,
        'x' : crop_summary_N['N'][0:10].sort_values()
    }

    last = {
        'y' : crop_summary_N['N'][-10:].index,
        'x' : crop_summary_N['N'][-10:]
    }

    fig.add_trace(
        go.Bar(top,
               name="Most nitrogen required",
               marker_color=random.choice(colorarr),
               orientation='h',
              text=top['x']),
        
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(last,
               name="Least nitrogen required",
               marker_color=random.choice(colorarr),
               orientation='h',
              text=last['x']),
        row=1, col=2
    )
    fig.update_traces(texttemplate='%{text}', textposition='inside')
    fig.update_layout(title_text="Nitrogen (N)",
                      plot_bgcolor='white',
                      font_size=12, 
                      font_color='black',
                     height=500)'''

    #fig.update_xaxes(showgrid=False)
    #fig.update_yaxes(showgrid=False)
    #fig.show()
    #graph1
    ##############################
    ##Phosphorus Analysis
    crop_summary_P = crop_summary.sort_values(by='P', ascending=False)
  
    '''fig = make_subplots(rows=1, cols=2)

    top = {
        'y' : crop_summary_P['P'][0:10].sort_values().index,
        'x' : crop_summary_P['P'][0:10].sort_values()
    }

    last = {
        'y' : crop_summary_P['P'][-10:].index,
        'x' : crop_summary_P['P'][-10:]
    }

    fig.add_trace(
        go.Bar(top,
               name="Most phosphorus required",
               marker_color=random.choice(colorarr),
               orientation='h',
              text=top['x']),
        
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(last,
               name="Least phosphorus required",
               marker_color=random.choice(colorarr),
               orientation='h',
              text=last['x']),
        row=1, col=2
    )
    fig.update_traces(texttemplate='%{text}', textposition='inside')
    fig.update_layout(title_text="Phosphorus (P)",
                      plot_bgcolor='white',
                      font_size=12, 
                      font_color='black',
                     height=500)

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)'''
    #fig.show()
    #graph2
    #######################
    ##Potassium analysis
    crop_summary_K = crop_summary.sort_values(by='K', ascending=False)
  
    '''fig = make_subplots(rows=1, cols=2)

    top = {
        'y' : crop_summary_K['K'][0:10].sort_values().index,
        'x' : crop_summary_K['K'][0:10].sort_values()
    }

    last = {
        'y' : crop_summary_K['K'][-10:].index,
        'x' : crop_summary_K['K'][-10:]
    }

    fig.add_trace(
        go.Bar(top,
               name="Most potassium required",
               marker_color=random.choice(colorarr),
               orientation='h',
              text=top['x']),
        
        row=1, col=1
    )

    fig.add_trace(
        go.Bar(last,
               name="Least potassium required",
               marker_color=random.choice(colorarr),
               orientation='h',
              text=last['x']),
        row=1, col=2
    )
    fig.update_traces(texttemplate='%{text}', textposition='inside')
    fig.update_layout(title_text="Potassium (K)",
                      plot_bgcolor='white',
                      font_size=12, 
                      font_color='black',
                     height=500)

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)'''
    #fig.show()
    #graph3
    #########################
    ##N, P, K values comparision between crops
    '''fig = go.Figure()
    fig.add_trace(go.Bar(
        x=crop_summary.index,
        y=crop_summary['N'],
        name='Nitrogen',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=crop_summary.index,
        y=crop_summary['P'],
        name='Phosphorous',
        marker_color='lightsalmon'
    ))
    fig.add_trace(go.Bar(
        x=crop_summary.index,
        y=crop_summary['K'],
        name='Potash',
        marker_color='crimson'
    ))

    fig.update_layout(title="N, P, K values comparision between crops",
                      plot_bgcolor='white',
                      barmode='group',
                      xaxis_tickangle=-45)'''

    #fig.show()
    #graph4
    #####################
    ##NPK ratio for rice, cotton, jute, maize, lentil
    labels = ['Nitrogen(N)','Phosphorous(P)','Potash(K)']
    '''fig = make_subplots(rows=1, cols=5, specs=[[{'type':'domain'}, {'type':'domain'},
                                                {'type':'domain'}, {'type':'domain'}, 
                                                {'type':'domain'}]])

    rice_npk = crop_summary[crop_summary.index=='rice']
    values = [rice_npk['N'][0], rice_npk['P'][0], rice_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Rice"),1, 1)

    cotton_npk = crop_summary[crop_summary.index=='cotton']
    values = [cotton_npk['N'][0], cotton_npk['P'][0], cotton_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Cotton"),1, 2)

    jute_npk = crop_summary[crop_summary.index=='jute']
    values = [jute_npk['N'][0], jute_npk['P'][0], jute_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Jute"),1, 3)

    maize_npk = crop_summary[crop_summary.index=='maize']
    values = [maize_npk['N'][0], maize_npk['P'][0], maize_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Maize"),1, 4)

    lentil_npk = crop_summary[crop_summary.index=='lentil']
    values = [lentil_npk['N'][0], lentil_npk['P'][0], lentil_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Lentil"),1, 5)

    fig.update_traces(hole=.4, hoverinfo="label+percent+name")
    fig.update_layout(
        title_text="NPK ratio for rice, cotton, jute, maize, lentil",
        annotations=[dict(text='Rice',x=0.06,y=0.8, font_size=15, showarrow=False),
                     dict(text='Cotton',x=0.26,y=0.8, font_size=15, showarrow=False),
                     dict(text='Jute',x=0.50,y=0.8, font_size=15, showarrow=False),
                     dict(text='Maize',x=0.74,y=0.8, font_size=15, showarrow=False),
                    dict(text='Lentil',x=0.94,y=0.8, font_size=15, showarrow=False)])'''
    #fig.show()
    #graph5
    #############
    ##NPK ratio for fruits
    labels = ['Nitrogen(N)','Phosphorous(P)','Potash(K)']
    specs = [[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}],[
             {'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}, {'type':'domain'}]]
    '''fig = make_subplots(rows=2, cols=5, specs=specs)
    cafe_colors =  ['rgb(255, 128, 0)', 'rgb(0, 153, 204)', 'rgb(173, 173, 133)']

    apple_npk = crop_summary[crop_summary.index=='apple']
    values = [apple_npk['N'][0], apple_npk['P'][0], apple_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Apple", marker_colors=cafe_colors),1, 1)

    banana_npk = crop_summary[crop_summary.index=='banana']
    values = [banana_npk['N'][0], banana_npk['P'][0], banana_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Banana", marker_colors=cafe_colors),1, 2)

    grapes_npk = crop_summary[crop_summary.index=='grapes']
    values = [grapes_npk['N'][0], grapes_npk['P'][0], grapes_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Grapes", marker_colors=cafe_colors),1, 3)

    orange_npk = crop_summary[crop_summary.index=='orange']
    values = [orange_npk['N'][0], orange_npk['P'][0], orange_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Orange", marker_colors=cafe_colors),1, 4)

    mango_npk = crop_summary[crop_summary.index=='mango']
    values = [mango_npk['N'][0], mango_npk['P'][0], mango_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Mango", marker_colors=cafe_colors),1, 5)

    coconut_npk = crop_summary[crop_summary.index=='coconut']
    values = [coconut_npk['N'][0], coconut_npk['P'][0], coconut_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Coconut", marker_colors=cafe_colors),2, 1)

    papaya_npk = crop_summary[crop_summary.index=='papaya']
    values = [papaya_npk['N'][0], papaya_npk['P'][0], papaya_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Papaya", marker_colors=cafe_colors),2, 2)

    pomegranate_npk = crop_summary[crop_summary.index=='pomegranate']
    values = [pomegranate_npk['N'][0], pomegranate_npk['P'][0], pomegranate_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Pomegranate", marker_colors=cafe_colors),2, 3)

    watermelon_npk = crop_summary[crop_summary.index=='watermelon']
    values = [watermelon_npk['N'][0], watermelon_npk['P'][0], watermelon_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Watermelon", marker_colors=cafe_colors),2, 4)

    muskmelon_npk = crop_summary[crop_summary.index=='muskmelon']
    values = [muskmelon_npk['N'][0], muskmelon_npk['P'][0], muskmelon_npk['K'][0]]
    fig.add_trace(go.Pie(labels=labels, values=values,name="Muskmelon", marker_colors=cafe_colors),2, 5)

    fig.update_layout(
        title_text="NPK ratio for fruits",
        annotations=[dict(text='Apple',x=0.06,y=1.08, font_size=15, showarrow=False),
                     dict(text='Banana',x=0.26,y=1.08, font_size=15, showarrow=False),
                     dict(text='Grapes',x=0.50,y=1.08, font_size=15, showarrow=False),
                     dict(text='Orange',x=0.74,y=1.08, font_size=15, showarrow=False),
                    dict(text='Mango',x=0.94,y=1.08, font_size=15, showarrow=False),
                    dict(text='Coconut',x=0.06,y=0.46, font_size=15, showarrow=False),
                     dict(text='Papaya',x=0.26,y=0.46, font_size=15, showarrow=False),
                     dict(text='Pomegranate',x=0.50,y=0.46, font_size=15, showarrow=False),
                     dict(text='Watermelon',x=0.74,y=0.46, font_size=15, showarrow=False),
                    dict(text='Muskmelon',x=0.94,y=0.46, font_size=15, showarrow=False)])'''
    #fig.show()
    #graph6
    ##############
    crop_scatter = cropdf[(cropdf['label']=='rice') | 
                      (cropdf['label']=='jute') | 
                      (cropdf['label']=='cotton') |
                     (cropdf['label']=='maize') |
                     (cropdf['label']=='lentil')]

    '''fig = px.scatter(crop_scatter, x="temperature", y="humidity", color="label", symbol="label")
    fig.update_layout(plot_bgcolor='white')
    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)'''

    #fig.show()
    #graph7
    ###################
    '''fig = px.bar(crop_summary, x=crop_summary.index, y=["rainfall", "temperature", "humidity"])
    fig.update_layout(title_text="Comparision between rainfall, temerature and humidity",
                      plot_bgcolor='white',
                     height=500)

    fig.update_xaxes(showgrid=False)
    fig.update_yaxes(showgrid=False)'''
    #fig.show()
    #graph8
    ####################
    ##Correlation between different features
    #fig, ax = plt.subplots(1, 1, figsize=(15, 9))
    #sns.heatmap(cropdf.corr(), annot=True,cmap='Wistia' )
    #ax.set(xlabel='features')
    #ax.set(ylabel='features')

    #plt.title('Correlation between different features', fontsize = 15, c='black')
    #plt.show()
    #graph9
    ###################
    #Declare independent and target variables
    X = cropdf.drop('label', axis=1)
    y = cropdf['label']
    #Split dataset into training and test set
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.3,
                                                        shuffle = True, random_state = 0)
    #LightGBM Model Building and Training
    # build the lightgbm model
    

    model = lgb.LGBMClassifier()
    get_result=model.fit(X_train, y_train)
    print(get_result)
    #Model Prediction
    # predict the results
    y_pred=model.predict(X_test)
    #View Accuracy
    # view accuracy
    

    accuracy=accuracy_score(y_pred, y_test)
    print('accuracy score: {0:0.4f}'.format(accuracy_score(y_test, y_pred)))
    #Compare train and test set accuracy
    y_pred_train = model.predict(X_train)
    print('Training-set accuracy score: {0:0.4f}'. format(accuracy_score(y_train, y_pred_train)))
    #Check for Overfitting
    # print the scores on training and test set

    print('Training set score: {:.4f}'.format(model.score(X_train, y_train)))
    print('Test set score: {:.4f}'.format(model.score(X_test, y_test)))
    #Confusion-matrix
    # view confusion-matrix
    # Print the Confusion Matrix and slice it into four pieces

    
    cm = confusion_matrix(y_test, y_pred)

    #plt.figure(figsize=(15,15))
    #sns.heatmap(cm, annot=True, fmt=".0f", linewidths=.5, square = True, cmap = 'Blues');
    #plt.ylabel('Actual label');
    #plt.xlabel('Predicted label');
    #all_sample_title = 'Confusion Matrix - score:'+str(accuracy_score(y_test,y_pred))
    ##plt.title(all_sample_title, size = 15);
    ##plt.show()
    
    return render_template('process3.html')
##LSTM
def load_data(stock, seq_len):
    amount_of_features = len(stock.columns)
    data = stock.as_matrix() #pd.DataFrame(stock)
    sequence_length = seq_len + 1
    result = []
    for index in range(len(data) - sequence_length):
        result.append(data[index: index + sequence_length])

    result = np.array(result)
    row = round(0.9 * result.shape[0])
    train = result[:int(row), :]
    x_train = train[:, :-1]
    y_train = train[:, -1][:,-1]
    x_test = result[int(row):, :-1]
    y_test = result[int(row):, -1][:,-1]

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], amount_of_features))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], amount_of_features))  

    return [x_train, y_train, x_test, y_test]

def build_model(layers):
    model = Sequential()

    model.add(LSTM(
        input_dim=layers[0],
        output_dim=layers[1],
        return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(
        layers[2],
        return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(
        output_dim=layers[2]))
    model.add(Activation("linear"))

    start = time.time()
    model.compile(loss="mse", optimizer="rmsprop",metrics=['accuracy'])
    print("Compilation Time : ", time.time() - start)
    return model

def build_model2(layers):
        d = 0.2
        model = Sequential()
        model.add(LSTM(128, input_shape=(layers[1], layers[0]), return_sequences=True))
        model.add(Dropout(d))
        model.add(LSTM(64, input_shape=(layers[1], layers[0]), return_sequences=False))
        model.add(Dropout(d))
        model.add(Dense(16,init='uniform',activation='relu'))        
        model.add(Dense(1,init='uniform',activation='linear'))
        model.compile(loss='mse',optimizer='adam',metrics=['accuracy'])
        return model

##########################
@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)



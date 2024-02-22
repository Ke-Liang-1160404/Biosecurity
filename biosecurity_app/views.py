from biosecurity_app import app
from flask import render_template, request, redirect, url_for,session
import mysql.connector
from mysql.connector import FieldType
import connect
from flask_hashing import Hashing

dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

@app.route("/")
def index ():
    return render_template('base.html') 


@app.route("/home")
def home():
   if 'username' in session:
      return render_template('home.html', username=session['username'])
   else:
      return render_template('home.html') 
   

@app.route('/')
def login():
    if request.method =="POST":
        username=request.form['username']
        pwd=request.form['password']
        connection = getCursor()
        connection.execute('select * from staff_admin ')
        staff=connection.fetchall()
        print(staff)
        return render_template('home.html',staff=staff) 

        




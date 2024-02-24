from biosecurity_app import app
from flask import render_template, request, redirect, url_for,session
import mysql.connector
from mysql.connector import FieldType
import connect
from flask_hashing import Hashing
from datetime import datetime
import re


hashing = Hashing(app)
app.secret_key = 'your secret key'

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
   

@app.route('/register', methods=['POST','GET'])
def register():
    msg=''
    if request.method == "GET":
      return render_template('register.html')
      
    elif request.method =='POST':  
      username=request.form.get('username')
      email=request.form.get('email')
      password=request.form.get('password')
      firstname=request.form.get('firstname')
      lastname=request.form.get('lastname')
      address=request.form.get('address')
      phone=request.form.get('phone')
      date=datetime.today().strftime("%Y-%m-%d")
      hashed=hashing.hash_value(password, salt="abcd")
      print(request.form)
      print(date)
      connection=getCursor()
      connection.execute("Select * from apiarists WHERE username= %s ", (username, ))
      user=connection.fetchone()
      connection.execute("Select * from apiarists WHERE email= %s", (email,))
      email_repeat=connection.fetchone()
      pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
      login=False
      registered=False
      if not re.match(pattern ,password):
         msg="Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character, and should be at least 8 characters long."
      elif user:
         msg='User already existed'
      elif email_repeat:
         msg=""
         login=True
      elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
      elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'   
      else:
          sql="""INSERT INTO apiarists (first_name, last_name, username, password, email, address, phone,date_joined,  status) VALUES ( %s, %s, %s,%s,%s,%s,%s,%s,1)
          """
          connection.execute(sql, (firstname, lastname, username, hashed, email, address, phone, date))
          msg="Registered account successfully"
          registered=True

    return render_template('register.html', msg=msg, login=login, registered=registered) 

        




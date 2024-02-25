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
    print("TRAILING_SLASH configuration:", app.url_map.strict_slashes)
    return render_template('base.html') 


@app.route("/home")
def home():
   if 'username' in session:
      return render_template('home.html', username=session['username'])
   else:
      return render_template('home.html') 
   

@app.route('/register', methods=['POST','GET'])
def register():
    # set default prompt message to empty string
    msg=''
    # Render the register the form
    if request.method == "GET":
      return render_template('register.html')
    #get the input from the form using POST method  
    elif request.method =='POST':  
      username=request.form.get('username')
      email=request.form.get('email')
      password=request.form.get('password')
      firstname=request.form.get('firstname')
      lastname=request.form.get('lastname')
      address=request.form.get('address')
      phone=request.form.get('phone')
      date=datetime.today().strftime("%Y-%m-%d")
      #hashing the password to hashed password
      hashed=hashing.hash_value(password, salt="abcd")
      #query the input and compare the input user and email with existed user and email address to check if they are already in the database
      connection=getCursor()
      connection.execute("Select * from apiarists WHERE username= %s ", (username, ))
      user=connection.fetchone()
      connection.execute("Select * from apiarists WHERE email= %s", (email,))
      email_repeat=connection.fetchone()
      #using regular expression to validate password to have Upper case, lover case, number, special sign and at least 8 characters within it
      pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
      toLogin=False
      registered=False
      #haddle different validations and set the  message to prompt related information
      if not re.match(pattern ,password):
         msg="Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character, and should be at least 8 characters long."
      elif user:
         msg='User already existed'
      elif email_repeat:
         msg=""
         toLogin=True
      elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
      elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'   
      #after validation, insert the input into database
      else:
          sql="""INSERT INTO apiarists (first_name, last_name, username, password, email, address, phone,date_joined,  status) VALUES ( %s, %s, %s,%s,%s,%s,%s,%s,1)
          """
          connection.execute(sql, (firstname, lastname, username, hashed, email, address, phone, date))
          msg="Registered account successfully"
          registered=True

    return render_template('register.html', msg=msg, toLogin=toLogin, registered=registered) 

        
@app.route("/signin")
def signin():
      return render_template('signin.html')



from biosecurity_app import app
from flask import render_template, request, redirect, url_for,session
import mysql.connector
from mysql.connector import FieldType
import connect
from flask_hashing import Hashing
from datetime import datetime, timedelta
import re


hashing = Hashing(app)
app.secret_key = 'hello'
app.url_map.strict_slashes = False 
app.permanent_session_lifetime=timedelta(minutes =5)
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

# check which role is in session
def redirect_based_on_role(html_file):
    if "user" in session:
        return redirect(url_for("user"))
    elif "staff" in session:
        return redirect(url_for("staff"))
    elif "admin" in session:
        return redirect(url_for("admin"))
    else:
        return render_template(html_file)


@app.route("/")
def index():
    return redirect_based_on_role('base.html')


@app.route("/home")
def home():
   return redirect_based_on_role('home.html')
   

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

        
@app.route("/login", methods=['POST','GET'])
def login():
      msg=''
      if request.method=='POST':
          session.permanent = True
          #---------get username and password from frontend -----------#
          username=request.form.get('username')
          password=request.form.get('password')
          #--------------------#
          #--------hassing the password------------#
          hashed=hashing.hash_value(password, salt="abcd")
         
          #---------query the apiarist from database-----------#

          connection=getCursor()
          connection.execute("select username,password from apiarists where username=%s and password=%s;", (username,hashed,))
          user=connection.fetchone()
         
          #---------query the staff from database-----------#


          connection.execute("select username,password,position from staff_admin where username=%s and password=%s and position='staff';",(username,hashed,))
          staff=connection.fetchone()

          #---------query the admin from database-----------#

          connection.execute("select username,password,position from staff_admin where username=%s and password=%s and position='admin';",(username,hashed,))
          admin=connection.fetchone()

          #---------compared the user input to check user's role if no position, then user is an apiarists-----------#
      
          if user is not None and user[0] == username:
            session["user"] =username
            return redirect(url_for("user", user=user))
          
          #---------check user's position, staff or admin-----------#
          elif staff is not None and staff[0] == username:
            session["staff"] =username
            return redirect(url_for("staff",staff=staff))
          elif admin is not None and admin[0] == username:
            session["admin"] =username
            return redirect(url_for("admin",admin=admin))
          
          #---------Not matching any role from database-----------#
          
          else:
             msg='username or password not correct Please try again'
             return render_template("login.html", msg=msg)
      else:
          return redirect_based_on_role('login.html')



@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("staff", None)
    session.pop("admin", None)
    return redirect(url_for("login")) 
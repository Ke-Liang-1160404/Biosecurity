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
app.permanent_session_lifetime=timedelta(hours =5)
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

## Password Check###
def check_password(password):
         msg=""
         pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
         if not re.match(pattern ,password):
            msg="Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character, and should be at least 8 characters long."
 

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
    

def choosing_role():
    if "user" in session:
        user=session["user"]
        return user
    elif "staff" in session:
        staff = session["staff"] 
        return staff
    elif "admin" in session:
        admin = session["admin"] 
        return admin


    
def render_login_or_register(registered,toLogin, msg, username):
    if toLogin:
        return render_template('login.html', msg=msg, toLogin=toLogin, registered=registered, username=username) 
    else:
        return render_template("register.html", msg=msg, toLogin=toLogin)

@app.route("/")
def index():
    return redirect_based_on_role('home.html')

@app.route("/reference")
def reference():
    choosing_role()
    print(choosing_role())

    return render_template('reference.html', user=choosing_role())

@app.route("/home")
def home():
    choosing_role()
    print(choosing_role())
    return render_template('home.html', user=choosing_role())
   

@app.route('/register', methods=['POST','GET'])
def register():
    if "user" in session:
        return redirect(url_for("user"))
    elif "staff" in session:
        return redirect(url_for("staff"))
    elif "admin" in session:
        return redirect(url_for("admin"))
    # set default prompt message to empty string
    msg=''
    # Render the register the form
    if request.method == "GET":
      haha=hashing.hash_value("password1", salt="abcd")
      print(haha)
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
         print(hashed)
         #query the input and compare the input user and email with existed user and email address to check if they are already in the database
         connection=getCursor()
         connection.execute("Select * from apiarists WHERE username= %s ", (username, ))
         user=connection.fetchone()
         connection.execute("Select * from apiarists WHERE email= %s", (email,))
         email_repeat=connection.fetchone()
         #using regular expression to validate password to have Upper case, lover case, number, special sign and at least 8 characters within it
         toLogin=False
         registered=False
         #haddle different validations and set the  message to prompt related information
         pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
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

          registered=True
          toLogin=True
          username=username
    return render_login_or_register(msg=msg, toLogin=toLogin, registered=registered, username= username) 

        
@app.route("/login", methods=['POST','GET'])
def login():
      toLogin=True
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
          connection.execute("select username,password from apiarists where username=%s and password=%s and status=1;", (username,hashed,))
          user=connection.fetchone()
          connection.execute("select username,password from apiarists where username=%s and password=%s and status=0;", (username,hashed,))
          inactive_user=connection.fetchone()
          #---------query the staff from database-----------#


          connection.execute("select username,password,position from staff_admin where username=%s and password=%s and position != 'admin' and status=1;",(username,hashed,))
          staff=connection.fetchone()
          connection.execute("select username,password,position from staff_admin where username=%s and password=%s and status=0;", (username,hashed,))
          inactive_staff=connection.fetchone()

          #---------query the admin from database-----------#

          connection.execute("select username,password,position from staff_admin where username=%s and password=%s and position='admin';",(username,hashed,))
          admin=connection.fetchone()
       

          #---------compared the user input to check user's role if no position, then user is an apiarists-----------#
      
          if user is not None and user[0] == username:
            session["user"] =username
            return redirect(url_for("home", user=user))
          
          #---------check user's position, staff or admin-----------#
          elif staff is not None and staff[0] == username:
            session["staff"] =username
            return redirect(url_for("home",staff=staff))
          elif admin is not None and admin[0] == username:
            session["admin"] =username
            return redirect(url_for("home",admin=admin))
          elif inactive_user is not None and inactive_user[0] == username:
             msg='user is not avtive please conntact an admin to activate your account admin email: john.murray123@admin.com'
             
             return render_template("login.html", msg=msg, toLogin=toLogin)
          elif inactive_staff is not None and inactive_staff[0] == username:
             msg='staff account is not avtive please conntact an admin to activate your account admin email: john.murray123@admin.com'
             
             return render_template("login.html", msg=msg, toLogin=toLogin)

          
          #---------Not matching any role from database-----------#
          
          else:
             msg='username or password not correct, Please try again'
             return render_template("login.html", msg=msg, toLogin=toLogin)
      else:
          return redirect_based_on_role('login.html')



@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("staff", None)
    session.pop("admin", None)
    return redirect(url_for("login")) 


def getAllApiarists():
    sql="""Select apiarists_id, username, first_name,last_name, email, phone, address, date_joined, status from apiarists"""
    connection=getCursor()
    connection.execute(sql)
    allApiarists=connection.fetchall()


    return allApiarists



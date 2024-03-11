from biosecurity_app import app
from flask import render_template, request, redirect, url_for,session
import mysql.connector
from mysql.connector import FieldType
import connect
from flask_hashing import Hashing
from datetime import datetime
import re
from biosecurity_app.staff_views import edit_apiarist
from biosecurity_app.views import check_password



hashing = Hashing(app)
app.secret_key = 'hello'
app.url_map.strict_slashes = False 
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
def getUser():
    username = session["user"]
    print(username)
    connection=getCursor()
    connection.execute("Select * from apiarists where username=%s",(username,))
    apiarist=connection.fetchone()
    return apiarist

@app.route("/apiarists/dashboard")
def apiarists_dashboard ():
      return "Hello Apiarists"

@app.route("/apiarists/profile")
def apiarists_profile():
      return "<h1>Apiarists Profile</h1>"



@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]  
        return render_template("managingUser.html", user=user)

    else:
       
        return redirect(url_for("login"))
    
@app.route("/user/profile")
def self_managing():
    
    if "user" in session:
        user = session["user"]  
        return render_template("user.html",apiarist=getUser(),user=user)
    else:
        return redirect(url_for("login"))
    
@app.route("/user/profile/edit", methods=["POST"])
def edit_profile():
  if "user" in session:
        user = session["user"] 
  edit_apiarist()
  return redirect(url_for('staffApiarists',user=user))


@app.route("/user/profile/password")
def password():
  if "user" in session:
        user = session["user"] 
  return render_template("password.html", user=user)

@app.route("/user/profile/password/new", methods=["POST"])
def edit_password():
  msg=""
  if "user" in session:
   username = session["user"] 
   if request.method =='POST':

     getUser()
     oldPassword=request.form.get("old_password")
     newPassword=request.form.get("new_password")
     reNewPassword=request.form.get("re_new_password")
     hashed_old=hashing.hash_value(oldPassword, salt="abcd")
     hashed_new=hashing.hash_value(newPassword, salt="abcd")

     connection=getCursor()
     connection.execute("SELECT password from apiarists where username=%s;", (username,))
     password=connection.fetchone()
     print ("hashed", hashed_old)
     print ("password", password[0])
     password_reset=False
     alert=False
     if hashed_old == password[0]:
         if newPassword == reNewPassword:

            pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
            if not re.match(pattern ,newPassword):
                   print("Password validate")
                   alert=True
                   msg="Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character, and should be at least 8 characters long."
                   return render_template("password.html", msg=msg, user=user, alert=alert)
            else:
             connection.execute("UPDATE apiarists SET password=%s where username=%s;", (hashed_new,username))
             msg="You have updated your password successfully"
             password_reset=True
             return render_template("user.html", msg=msg,user=username, password_reset=password_reset, apiarist=getUser())

         else:
             msg ="Please confrim your re-typed password match the new password"
             print("new password dont match")
             alert=True
             return render_template("password.html", msg=msg, user=username, alert=alert)
     else:
         msg="Your password input was not correct, please try again"
         print("old password incorrect")
         alert=True
         return render_template("password.html", msg=msg,user=username, alert=alert)
    
        

  else:
        return redirect(url_for("login"))
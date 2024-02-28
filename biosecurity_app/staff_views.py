from biosecurity_app import app
from flask import render_template, request, redirect, url_for,session
import mysql.connector
from mysql.connector import FieldType
import connect
from flask_hashing import Hashing
from datetime import datetime
import re
from biosecurity_app.views import getAllApiarists


hashing = Hashing(app)
app.secret_key = 'hello'
app.url_map.strict_slashes = False 
dbconn = None
connection = None

@app.route("/staff/dashboard")
def staff_dashboard ():
      return "Hello Staff"

@app.route("/staff/profile")
def staff_profile():
        connection = getCursor()
        connection.execute('select * from staff_admin ')
        staff=connection.fetchall()
        print(staff)
        return render_template('home.html',staff=staff) 

@app.route("/staff")
def staff():
    if "staff" in session:
        staff = session["staff"]  
        return render_template("staff.html", staff=staff)
    else:
       
        return redirect(url_for("login"))
    
@app.route("/staff/apiarists")
def staffApiarists():
   getAllApiarists()
   return render_template("editUser.html", allApiarists=getAllApiarists())
        
    
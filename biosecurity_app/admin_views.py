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



@app.route("/admin/dashboard")
def admin_dashboard ():
      return "Hello Admin"

@app.route("/admin/profile")
def admin_profile():
      return "<h1>Admin Profile</h1>"


@app.route("/admin")
def admin():
    if "admin" in session:
        admin = session["admin"]  
        return render_template("admin.html", admin=admin)

    else:
       
        return redirect(url_for("login"))
    
@app.route("/admin/apiarists")
def adminApiarists():
        getAllApiarists()
        
        return render_template("editUser.html", allApiarists=getAllApiarists())
    
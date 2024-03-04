from biosecurity_app import app
from flask import render_template, request, redirect, url_for,session
import mysql.connector
from mysql.connector import FieldType
import connect
from flask_hashing import Hashing
from datetime import datetime
import re
from biosecurity_app.views import getAllApiarists,getCursor
from biosecurity_app.staff_views import get_single_apiarist




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
        if "admin" in session:
          admin = session["admin"]  
          return render_template("allUser.html", allApiarists=getAllApiarists(), admin=admin)
        else:
       
          return redirect(url_for("login"))
        

@app.route("/admin/apiarists/<id>")
def admin_single_apiarist(id):
     get_single_apiarist(id)
     if "admin" in session:
        admin = session["admin"]
        return render_template("allUser.html", apiarist=get_single_apiarist(id), admin=admin)
     else:
        return redirect(url_for("login"))
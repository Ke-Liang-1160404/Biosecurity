from biosecurity_app import app
from flask import render_template, request, redirect, url_for,session
import mysql.connector
from mysql.connector import FieldType
import connect
from flask_hashing import Hashing
from datetime import datetime
import re


hashing = Hashing(app)
app.secret_key = 'hello'
app.url_map.strict_slashes = False 
dbconn = None
connection = None

def getCursor():
    global dbconn
    global connection
    connection = mysql.connector.connect(admin=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

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
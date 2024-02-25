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
    connection = mysql.connector.connect(user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
    dbconn = connection.cursor()
    return dbconn

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
        return f"<h1>{user}</h1>"
    else:
       
        return redirect(url_for("login"))
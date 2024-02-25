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
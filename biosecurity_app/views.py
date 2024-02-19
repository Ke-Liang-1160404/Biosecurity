from biosecurity_app import app
from flask import render_template
import mysql.connector
from mysql.connector import FieldType
import connect

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
      return "Hello World"

@app.route("/home")
def home():
   
      return render_template('home.html')




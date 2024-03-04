from biosecurity_app import app
from flask import Flask,render_template, request, redirect, url_for,session
import mysql.connector
from mysql.connector import FieldType
import connect
from flask_hashing import Hashing
from datetime import datetime
import re
from biosecurity_app.views import getAllApiarists,getCursor


hashing = Hashing(app)
app.secret_key = 'hello'
app.url_map.strict_slashes = False 
dbconn = None
connection = None




def get_single_apiarist(id):
    connection = getCursor()
    connection.execute("SELECT * FROM apiarists WHERE apiarists_id = %s;", (id,))
    apiarist = connection.fetchone()
    return apiarist

def edit_apiarist():
   if request.method == "POST":
      address=request.form.get("address")
      phone=request.form.get("phone")
      email=request.form.get("email")
      status=request.form.get("status")
      id=request.form.get("id")
      print(address,phone,email,status,email)
      connection=getCursor()
      sql="""UPDATE apiarists SET address=%s,phone=%s,email=%s,status=%s where apiarists_id=%s;"""
      connection.execute(sql,(address,phone,email,status,id,))
     
   

@app.route("/staff/dashboard")
def staff_dashboard ():
      return "Hello Staff"

@app.route("/staff/profile")
def staff_profile():
        connection = getCursor()
        connection.execute('select * from staff_admin;')
        staff=connection.fetchall()
        print(staff)
        return render_template('home.html',staff=staff) 

@app.route("/staff")
def staff():
    if "staff" in session:
        staff = session["staff"]  
        return render_template("managingUser.html", staff=staff)
    else:
       
        return redirect(url_for("login"))
    
@app.route("/staff/apiarists")
def staffApiarists():
    
    if "staff" in session:
        staff = session["staff"]
        all_apiarists = getAllApiarists()

        return render_template("allUser.html", allApiarists=all_apiarists, staff=staff)
    else:
        return redirect(url_for("login"))
 
        
@app.route("/staff/apiarists/<id>")
def staff_single_apiarist(id):
    apiarist=get_single_apiarist(id)
    if "staff" in session:
        staff = session["staff"]
        return render_template("user.html", apiarist=apiarist, staff=staff)
    else:
        return redirect(url_for("login"))

@app.route("/staff/apiarists/edit", methods=["POST"])
def staffeditapiarist():
  edit_apiarist()
  return redirect(url_for('staffApiarists'))


    


from biosecurity_app import app
from flask import render_template, request, redirect, url_for,session
import mysql.connector
from mysql.connector import FieldType
import connect
from flask_hashing import Hashing
from datetime import datetime
import re
from biosecurity_app.views import getAllApiarists,getCursor
from biosecurity_app.staff_views import get_single_apiarist,edit_apiarist,getStaff,edit_staff
from biosecurity_app.apiarists_views import all_pest





hashing = Hashing(app)
app.secret_key = 'hello'
app.url_map.strict_slashes = False 
dbconn = None
connection = None





@app.route("/admin")
def admin():
    if "admin" in session:
        admin = session["admin"]  
        return render_template("managingUser.html", admin=admin)

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
        return render_template("user.html", apiarist=get_single_apiarist(id), admin=admin)
     else:
        return redirect(url_for("login"))
     

@app.route("/admin/apiarists/edit", methods=["POST"])
def admineditapiarist():
  edit_apiarist()
  return redirect(url_for('adminApiarists'))


@app.route("/admin/staff")
def adminStaff():
        connection=getCursor()
        connection.execute("SELECT staff_id,username,first_name,last_name,email,work_phone_number, address,hire_date,position,department,status from staff_admin where position !='admin';")
        allStaff=connection.fetchall()
        if "admin" in session:
          admin = session["admin"]  
          return render_template("allStaff.html", allStaff=allStaff, admin=admin)
        else:
       
          return redirect(url_for("login"))
        
@app.route("/admin/staff/<id>")
def admin_single_staff(id):
     connection = getCursor()
     connection.execute("SELECT * FROM staff_admin WHERE staff_id = %s;", (id,))
     staff = connection.fetchone()
     print(staff)
     if "admin" in session:
        admin = session["admin"]
        return render_template("staff.html", staff=staff, admin=admin)
     else:
        return redirect(url_for("login"))
     

@app.route("/admin/staff/edit", methods=["POST"])
def admin_edit_staff():
 if "admin" in session:
  admin = session["admin"]
  if request.method == "POST":
      address=request.form.get("address")
      phone=request.form.get("phone")
      email=request.form.get("email")
      status=request.form.get("status")
      position=request.form.get("position")
      department=request.form.get("department")

      id=request.form.get("id")
      print(address,phone,email,status,email)
      connection=getCursor()
      sql="""UPDATE staff_admin SET address=%s,work_phone_number=%s,email=%s,position=%s,department=%s,status=%s where staff_id=%s;"""
      connection.execute(sql,(address,phone,email,position,department,status,id,))
  return redirect(url_for('adminStaff', admin=admin))
 

@app.route("/admin/guide")
def guide_admin():
  if "admin" in session:
        admin = session["admin"] 
        all_pest()
        return render_template("guide.html", admin=admin, all_pest=all_pest())
  
  else:
        return redirect(url_for("login"))


@app.route("/admin/profile")
def admin_self_managing():
    
    if "admin" in session:
        admin = session["admin"]  
        return render_template("profile.html",role=getStaff("admin"),admin=admin)
    else:
        return redirect(url_for("login"))
    

@app.route("/admin/profile/edit", methods=["POST"])
def admin_edit_profile():
  if "admin" in session:
        admin = session["admin"] 
        edit_staff()
        msg="Information Updated"
        updated=True
        return redirect(url_for('staffApiarists',admin=admin,msg=msg, updated=updated))

  else:
        return redirect(url_for("login"))



@app.route("/admin/profile/password")
def admin_password():
  if "admin" in session:
        admin = session["admin"] 
  return render_template("password.html", admin=admin)
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

def get_single_pest(id):
    connection = getCursor()
    connection.execute("SELECT * FROM pest_disease left join images on id = pest_id WHERE id = %s;", (id,))
    pest = connection.fetchall()
    return pest

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

def edit_staff():
   if request.method == "POST":
      address=request.form.get("address")
      phone=request.form.get("phone")
      email=request.form.get("email")

      id=request.form.get("id")
      print(address,phone,email,email)
      connection=getCursor()
      sql="""UPDATE staff_admin SET address=%s,work_phone_number=%s,email=%s where staff_id=%s;"""
      connection.execute(sql,(address,phone,email,id,))
     
def all_pest():
        connection=getCursor()
        connection.execute("select * from pest_disease left join images on primary_image = image_id;")
        all_pest=connection.fetchall()
        return all_pest

def getStaff(role):
    username = session[role]
    print(username)
    connection=getCursor()
    connection.execute("Select * from staff_admin where username=%s",(username,))
    staff_admin=connection.fetchone()
    return staff_admin



@app.route("/staff")
def staff():
    if "staff" in session:
        staff = session["staff"]  
        return render_template("managingUser.html", staff=staff)
    else:
       
        return redirect(url_for("login"))
    
@app.route("/staff/apiarists")
def staffApiarists():
    updadted=False
    msg=""
    if "staff" in session:
        staff = session["staff"]
        all_apiarists = getAllApiarists()

        return render_template("allUser.html", allApiarists=all_apiarists, staff=staff,msg=msg,updadted=updadted )
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


    

@app.route("/staff/guide")
def guide_staff():
  if "staff" in session:
        staff = session["staff"] 
        all_pest()

       
        return render_template("guide.html", staff=staff, all_pest=all_pest() )

  else:
        return redirect(url_for("login"))


@app.route("/staff/profile")
def staff_self_managing():
    
    if "staff" in session:
        staff = session["staff"]  
        return render_template("profile.html",role=getStaff("staff"),staff=staff)
    else:
        return redirect(url_for("login"))
    
@app.route("/staff/profile/edit", methods=["POST"])
def staff_edit_profile():
  if "staff" in session:
        staff = session["staff"] 
        edit_staff()
        msg="Information Updated"
        updated=True
        return redirect(url_for('staffApiarists',staff=staff,msg=msg, updated=updated))

  else:
        return redirect(url_for("login"))
  

@app.route("/staff/profile/password")
def staff_password():
  if "staff" in session:
        staff = session["staff"] 
        return render_template("password.html", staff=staff)
  else:
        return redirect(url_for("login"))
  

@app.route("/staff/profile/password/new", methods=["POST"])
def staff_edit_password():
  msg=""
  if "staff" in session:
   username = session["staff"] 
   if request.method =='POST':

     getStaff("staff")

     oldPassword=request.form.get("old_password")
     newPassword=request.form.get("new_password")
     reNewPassword=request.form.get("re_new_password")
     hashed_old=hashing.hash_value(oldPassword, salt="abcd")
     hashed_new=hashing.hash_value(newPassword, salt="abcd")

     connection=getCursor()
     connection.execute("SELECT password from staff_admin where username=%s;", (username,))
     password=connection.fetchone()
     
     password_reset=False
     alert=False
     if hashed_old == password[0]:
         if newPassword == reNewPassword:

            pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
            if not re.match(pattern ,newPassword):

                   alert=True
                   msg="Password must contain at least one uppercase letter, one lowercase letter, one digit, and one special character, and should be at least 8 characters long."
                   return render_template("password.html", msg=msg, staff=staff, alert=alert)
            else:
             connection.execute("UPDATE staff_admin SET password=%s where username=%s;", (hashed_new,username))
             msg="You have updated your password successfully"
             password_reset=True
             return render_template("profile.html", msg=msg,user=username, password_reset=password_reset, role=getStaff("staff"))

         else:
             msg ="Please confrim your re-typed password match the new password"

             alert=True
             return render_template("password.html", msg=msg, user=username, alert=alert)
     else:
         msg="Your password input was not correct, please try again"

         alert=True
         return render_template("password.html", msg=msg,user=username, alert=alert)
    
        

  else:
        return redirect(url_for("login"))
  


@app.route("/staff/guide/<id>")
def staff_pest(id):

  if "staff" in session:
        staff = session["staff"] 

        return render_template("pest.html", pest=get_single_pest(id), staff=staff)
  else:
        return redirect(url_for("login"))
  
@app.route("/staff/guide/pest/edit", methods=['POST'])
def staff_pest_edit():
  changed= False
  if "staff" in session:
      if request.method =='POST':
        staff = session["staff"] 
        id=request.form.get("id")
        character=request.form.get("chracter")
        bio=request.form.get("bioDescription")
        symptoms=request.form.get("symptoms")
        image=request.form.get("image")
        
        
        connection=getCursor()
        connection.execute("select * from images where image_url=%s", (image,))
        updated_image=connection.fetchone()
        
        
        connection.execute("UPDATE pest_disease SET key_characteristics=%s, biology_description=%s, symptoms=%s,primary_image=%s where id=%s;", (character,bio,symptoms,updated_image[0],id,) )
        msg="successfully"
        changed=True
        return redirect(url_for("guide_staff", staff=staff, all_pest=all_pest(), msg=msg, changed=changed))
  else:
        return redirect(url_for("login"))
  





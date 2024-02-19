from biosecurity_app import app

@app.route("/staff/dashboard")
def staff_dashboard ():
      return "Hello Staff"

@app.route("/staff/profile")
def staff_profile():
      return "<h1>Staff Profile</h1>"
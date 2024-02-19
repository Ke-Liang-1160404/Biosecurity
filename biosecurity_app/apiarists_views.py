from biosecurity_app import app

@app.route("/apiarists/dashboard")
def apiarists_dashboard ():
      return "Hello Apiarists"

@app.route("/apiarists/profile")
def apiarists_profile():
      return "<h1>Apiarists Profile</h1>"




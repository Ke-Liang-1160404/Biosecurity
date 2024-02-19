from biosecurity_app import app

@app.route("/admin/dashboard")
def admin_dashboard ():
      return "Hello Admin"

@app.route("/admin/profile")
def admin_profile():
      return "<h1>Admin Profile</h1>"

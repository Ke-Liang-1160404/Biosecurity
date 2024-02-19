from biosecurity_app import app

@app.route("/")
def index ():
      return "Hello World"

@app.route("/about")
def about():
      return "<h1>About</h1>"




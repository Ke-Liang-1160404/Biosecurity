from flask import Flask

app= Flask(__name__)
app.url_map.strict_slashes = False  # Disable trailing slashes
from biosecurity_app import views
from biosecurity_app import admin_views
from biosecurity_app import staff_views
from biosecurity_app import apiarists_views
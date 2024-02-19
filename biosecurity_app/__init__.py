from flask import Flask

app= Flask(__name__)

from biosecurity_app import views
from biosecurity_app import admin_views
from biosecurity_app import staff_views
from biosecurity_app import apiarists_views
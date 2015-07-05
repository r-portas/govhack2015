__author__ = 'Ryan Lonergan'

from flask import Flask
app = Flask(__name__)
#app.config('config')

from website import views

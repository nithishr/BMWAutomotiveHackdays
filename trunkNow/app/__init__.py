__author__ = 'nithishr'

from flask import Flask

app = Flask(__name__)
from app import views

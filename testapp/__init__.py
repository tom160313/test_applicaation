from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('testapp.config') # 追加

db = SQLAlchemy(app)
from .models import employee  # 追加pytho

import testapp.views


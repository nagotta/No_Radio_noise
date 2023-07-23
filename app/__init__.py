import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('ep1_app.config')

db = SQLAlchemy(app)

from .models import Radio, Corner

import ep1_app.views 

def create_database():
    with app.app_context():
        db_file_path = app.config['SQLALCHEMY_DATABASE_URI'][10:]
        if not os.path.exists(db_file_path):
            db.create_all()

create_database()

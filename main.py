from flask import Flask
from application.database import db
import os

app=None

def create_app():
    app=Flask(__name__,template_folder="templates")
    CURRENT_DIR=os.path.dirname(os.path.abspath(__file__))
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(CURRENT_DIR,'db_directory','db.sqlite3')
    db.init_app(app)
    app.app_context().push()
    return app

app=create_app()

from application.controllers import *

if __name__=="__main__":
    app.debug=True
    app.run()
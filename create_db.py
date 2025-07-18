from main import app
from application.database import db

with app.app_context():
    db.create_all()
    print("Database and tables created successfully")
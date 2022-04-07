import os 

os.remove("db.sqlite3")

from app import db
db.create_all()
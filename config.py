from flask_sqlalchemy import SQLAlchemy

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Pitagora007%231@localhost:3306/micro_lecturi'
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy()

WEBSITE_URL = "http://127.0.0.1:5000"
from flask_sqlalchemy import SQLAlchemy

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Pitagora007#1@localhost:3306/micro_lecturi'
SQLALCHEMY_TRACK_MODIFICATIONS = False
db = SQLAlchemy()

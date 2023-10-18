from extensions import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    enabled = db.Column(db.Boolean, nullable=False)

    # Relationships
    verifications = db.relationship('UserVerification', backref='user', lazy=True)
    subscriptions = db.relationship('Subscription', backref='user', lazy=True)

class UserVerification(db.Model):
    __tablename__ = 'user_verification'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(255), unique=True, nullable=False)
    active_date = db.Column(db.DateTime, nullable=False)

class LectureCategory(db.Model):
    __tablename__ = 'lecture_category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True, nullable=False)

class Lecture(db.Model):
    __tablename__ = 'lecture'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    chunks = db.Column(db.Integer, nullable=False)
    id_category = db.Column(db.Integer, db.ForeignKey('lecture_category.id'), nullable=False)

    # Relationships
    subscriptions = db.relationship('Subscription', backref='lecture', lazy=True)

class Subscription(db.Model):
    __tablename__ = 'subscription'

    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    id_lecture = db.Column(db.Integer, db.ForeignKey('lecture.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    current_chunk = db.Column(db.Integer, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False)

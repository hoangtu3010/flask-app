from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Customers(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False)
    age = db.Column(db.Integer, nullable=True)
    career = db.Column(db.Text, nullable=True)
    income = db.Column(db.Float, nullable=True)

class Options(db.Model):
    __tablename__ = "options"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    questions_id = db.Column(db.Integer, db.ForeignKey(
        "questions.id"))
    questions = db.relationship("Questions", backref="options")

class Questions(db.Model):
    __tablename__ = "questions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)
    
class Answers(db.Model):
    __tablename__ = "answers"

    id = db.Column(db.Integer, primary_key=True)
    questions_id = db.Column(db.Integer, db.ForeignKey("questions.id"))
    questions = db.relationship("Questions", backref="questions")
    options_id = db.Column(db.Integer, db.ForeignKey("options.id"))
    options = db.relationship("Options", backref="options")
    customers_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    customers = db.relationship("Customers", backref="customers")
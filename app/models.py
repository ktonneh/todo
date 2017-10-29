from app import db;


class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    public_id = db.Column(db.String(50),unique=True)
    name = db.Column(db.String(50))
    password= db.Column(db.String(255))
    admin = db.Column(db.Boolean,default=False)


class Todo(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50))
    description = db.Column(db.String(200))
    status = db.Column(db.Boolean,default=False)
    user_id = db.Column(db.Integer)






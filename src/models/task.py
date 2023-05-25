from init_app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def __init__(self, name, type, created_at, status):
        self.name = name
        self.type = type
        self.created_at = created_at
        self.status = status

from . import db

class Assignment(db.Model):
    __tablename__ = 'assignments'
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(50), nullable=False)
    assignment_number = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, nullable=True)
    folder_path = db.Column(db.String(255), nullable=True)

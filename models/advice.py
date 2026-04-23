from db import db

class FinancialAdvice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    advice_text = db.Column(db.Text, nullable=False)
    generated_date = db.Column(db.DateTime, nullable=False)

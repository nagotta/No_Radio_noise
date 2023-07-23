'''
データベースのモデルを定義します。
具体的には、RadioChannelモデル（ラジオチャンネルの登録・削除を管理）と
Mailモデル（メール機能の管理）を定義する
'''
from flask_sqlalchemy import SQLAlchemy
from ep1_app import db

class Radio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    channel_type = db.Column(db.String(50))
    channel_id = db.Column(db.String(100))
    email = db.Column(db.String(120))
    corners = db.relationship('Corner', backref='radio')

class Corner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    radio_id = db.Column(db.Integer, db.ForeignKey('radio.id'))
    corner_name = db.Column(db.String(100))

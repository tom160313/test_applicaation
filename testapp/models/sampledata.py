from testapp import db
from datetime import datetime


class Sampledata(db.Model):
    __tablename__ = 'sampledata'
    id = db.Column(db.Integer, primary_key=True)  # システムで使う番号
    getdate = db.Column(db.Date)  # 日付
    gettime = db.Column(db.Time)  # 時間
    speed = db.Column(db.Integer)  # 運転速度
    itemno = db.Column(db.Integer)  # 品番
    peak = db.Column(db.Integer)  # 社歴
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)  # 作成日時
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)  # 更新日時
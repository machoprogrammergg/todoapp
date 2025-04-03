from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from . import db


class UserAccount(db.Model, UserMixin):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    tasks = db.relationship('TaskList')
    task_count = Column(Integer)

    def get_id(self):
        return str(self.id)

    def is_authenticated(self):
        return self.is_authenticated

    def is_active(self):
        return self.is_active

    def is_anonymous(self):
        return False  # Return False for authenticated users
        return f"<UserAccount {self.name}>"

class TaskList(db.Model):
    __tablename__ =  'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    note = Column(String)
    user_id = Column(Integer, ForeignKey('user_account.id'))
    time_stamp = Column(String)
    completed = Column(Boolean)
"""
learn flask models
"""
# pylint: disable=invalid-name, too-few-public-methods

from . import mydb

class Role(mydb.Model):
    """role"""
    __tablename__ = 'roles'
    uid = mydb.Column(mydb.Integer, primary_key=True)
    name = mydb.Column(mydb.String(64), unique=True)
    user = mydb.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(mydb.Model):
    """user"""
    __tablename__ = 'users'
    uid = mydb.Column(mydb.Integer, primary_key=True)
    username = mydb.Column(mydb.String(64), unique=True, index=True)
    role_id = mydb.Column(mydb.Integer, mydb.ForeignKey('roles.uid'))

    def __repr__(self):
        return '<User %r>' % self.username
        
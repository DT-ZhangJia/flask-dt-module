"""
learn flask models
"""
# pylint: disable=invalid-name, too-few-public-methods

from . import mydb, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Role(mydb.Model):
    """role"""
    __tablename__ = 'roles'
    uid = mydb.Column(mydb.Integer, primary_key=True)
    name = mydb.Column(mydb.String(64), unique=True)
    user = mydb.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

class User(UserMixin, mydb.Model):
    """user"""
    __tablename__ = 'users'
    uid = mydb.Column(mydb.Integer, primary_key=True)
    #id = uid #如果不手动设置这个id的参数，则get_id方法就报错，奇怪！
    username = mydb.Column(mydb.String(64), unique=True, index=True)
    email = mydb.Column(mydb.String(64), unique=True, index=True)
    passwd_hash = mydb.Column(mydb.String(128))
    role_id = mydb.Column(mydb.Integer, mydb.ForeignKey('roles.uid'))


    @property
    def passwd(self):
        raise AttributeError('无法读取')
    
    @passwd.setter
    def passwd(self, passwd):
        self.passwd_hash = generate_password_hash(passwd)

    def verify_passwd(self, passwd):
        return check_password_hash(self.passwd_hash, passwd)

    def get_id(self): #自己创建get_id方法，"override"覆盖usermixin里默认设置的返回self.id属性
        return self.uid #自设的user实例中的属性是uid

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) #这个回调函数难以理解，参见pocket内记载
"""
learn flask models
"""
# pylint: disable=invalid-name, too-few-public-methods, no-member
# no-member是为了避免flask_sqlalchemy无法读取尚未执行的程序中的类而报错


from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flask_login import UserMixin
from . import mydb, login_manager

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
    confirmed = mydb.Column(mydb.Boolean, default=False)

    @property
    def passwd(self):
        """设置无法读取密码属性"""
        raise AttributeError('无法读取')

    @passwd.setter
    def passwd(self, passwd):
        """生成密码离散值"""
        self.passwd_hash = generate_password_hash(passwd)

    def verify_passwd(self, passwd):
        """验证离散值密码"""
        return check_password_hash(self.passwd_hash, passwd)

    def get_id(self): #自己创建get_id方法，"override"覆盖usermixin里默认设置的返回self.id属性
        return self.uid #自设的user实例中的属性是uid

    def generate_confirmation_token(self, expiration=300):
        """生成注册确认令牌"""
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.uid})

    def confirm(self, token):
        """验证存在"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except: # pylint: disable=W0702
            return False
        if data.get('confirm') != self.uid:#这个检测有什么意义？
            return False
        self.confirmed = True
        mydb.session.add(self)
        return True

    def generate_resetpw_token(self, expiration=3600):
        """生成重置密码确认令牌"""
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.uid})

    def reset_password(self, token, new_password):
        """写入重置的新密码"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except: # pylint: disable=W0702
            return False
        if data.get('reset') != self.uid:#reset的时候需要核对邮箱与申请重置的是同一个用户
            return False
        #self.passwd = new_password
        self.passwd_hash = generate_password_hash(new_password)
        mydb.session.add(self)
        return True #放在这里难道是永恒为true？

    def __repr__(self):
        return '<User %r>' % self.username

@login_manager.user_loader
def load_user(user_id):
    """用户存在性回调函数"""
    return User.query.get(int(user_id)) #这个回调函数难以理解，参见pocket内记载

from flask import Blueprint,render_template,request,redirect,url_for
from flask_login import login_user,logout_user,login_required,current_user,UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
import data as dt

auth_bp = Blueprint('auth',__name__,url_prefix = '/')

@auth_bp.route('/register',methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        用户数据 = dt.执行查询("SElECT * FROM users WHERE username = %s",(username,))
        if 用户数据:
            return f'{username}已存在，请重新注册！'

        password_hash = generate_password_hash(password)
        dt.执行插入(
            'INSERT INTO users (username,password_hash,role) VALUES (%s,%s,"user")',
            (username,password_hash)
        )
        return redirect(url_for('auth.login'))
    return render_template('/register.html')


@auth_bp.route('login',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        用户数据 = dt.执行查询(
            "SElECT * FROM users WHERE username = %s",
            (username,)
        )
        if 用户数据 and check_password_hash(用户数据[0][2],password):
            用户对象 = user(用户数据[0][0],用户数据[0][1],用户数据[0][3])
            login_user(用户对象)
            return redirect(url_for('page.首页'))
        else:
            return '用户名或密码错误'
    return render_template('login.html') 

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

class user(UserMixin):
    def __init__(self,id,username,role):
        self.id = id
        self.username = username
        self.role = role

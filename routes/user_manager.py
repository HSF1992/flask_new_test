from flask import Flask,request,Blueprint,redirect,url_for,render_template
from flask_login import login_required,current_user
from werkzeug.security import check_password_hash,generate_password_hash
from routes.auth import user
import data as dt

user_manager_bp = Blueprint('user_manager',__name__,url_prefix ="/admin")

@user_manager_bp.route('update',methods =['POST','GET'])
@login_required
def update_password(user_id):
    if request.method == 'POST' and current_user.role == 'admin':
        password = request.form['password']
        row = dt.执行查询('SELECT password_hash FROM users WHERE id = %s',(user_id,))
        if  check_password_hash(row[0][0],password):
            return render_template('password_update.html')
        else:
            return redirect(url_for('page.message',message = "密码错误"))
    return render_template('/password_update.html')

@user_manager_bp.route('edit',methods = ['POST','GET'])
@login_required
def edit():
    if current_user.role != 'admin':
        return redirect(url_for('page.message',message = '您没有权限访问!'))
    if request.method == 'POST':
        username = request.form['username']
        role = request.form['role']
        dt.执行插入('UPDATE username = %s,role = %s FROM users WHERE id = %s',(username,role,user_id))
        return redirect(url_for('admin.admin'))
    return render_template('/edit.html')

@user_manager_bp.route('delete',methods = ['POST','GET'])
@login_required
def delete(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('page.message',message = '您暂无权限操作！'))
    if current_user.id == user_id:
        return redirect(url_for('page.message',message = '不能删除自己！'))
    dt.执行插入('DELETE FROM users WHERE id = %s',(user_id,))
    return redirect(url_for('admin.admin'))


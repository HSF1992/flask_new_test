from flask import Flask,request,Blueprint,redirect,url_for,render_template
from flask_login import login_required,current_user
from werkzeug.security import check_password_hash,generate_password_hash
from routes.auth import user
import data as dt

user_manager_bp = Blueprint('user_manager',__name__,url_prefix ="/admin")

@user_manager_bp.route('password_check/<int:user_id>',methods = ['POST','GET'])
@login_required
def password_check(user_id):
    if request.method == 'POST':
        password = request.form.get('password')
        if not password:
            return '错误，没有数据！'
        row = dt.执行查询('SELECT password_hash FROM users WHERE id = %s',(user_id,))
        if  check_password_hash(row[0][0],password):
            return render_template('password_update.html',user_id = user_id)
        else:
            return redirect(url_for('page.message',message = "密码错误"))
    return render_template('/password_check.html',user_id = user_id)

@user_manager_bp.route('password_update/<int:user_id>',methods=['POST','GET'])
@login_required
def password_update(user_id):
    if request.method == 'POST':
        password_new = request.form['password']
        i = dt.执行查询('SELECT password_hash FROM users WHERE id = %s',(user_id,))
        if check_password_hash(i[0][0],password_new):
            return redirect(url_for('page.message',message = "新密码不能与原密码一致！"))
        dt.执行插入('UPDATE users SET password_hash = %s WHERE id = %s',(password_new,user_id))
        return redirect(url_for('page.message',message = '更新成功!'))
    return render_template('/password_update.html')
@user_manager_bp.route('delete/<int:user_id>',methods = ['POST','GET'])
@login_required
def delete(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('page.message',message = '您暂无权限操作！'))
    if current_user.id == user_id:
        return redirect(url_for('page.message',message = '不能删除自己！'))
    dt.执行插入('DELETE FROM users WHERE id = %s',(user_id,))
    return redirect(url_for('page.message',message="删除成功！"))


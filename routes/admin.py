from flask import Flask,request,Blueprint
from flask_login import current_user,login_required
import data as dt

admin_bp = Blueprint('admin',__name__,url_prefix = '/')

@admin_bp.route('admin')
@login_required
def admin():
    if current_user.role != 'admin':
        return redirect(url_for('page.message',message = '暂无权限查看！'))
    数据 = dt.获取所有数据()
    用户信息 = dt.执行查询('SELECT * FROM users')
    return render_template('admin.html',用户信息 =用户信息,数据 = 数据)

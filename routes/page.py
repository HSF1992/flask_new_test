from flask import Blueprint,render_template,request,redirect,url_for
from flask_login import login_required,current_user
import data as dt
import service as sv
from datetime import datetime

page_bp = Blueprint('page',__name__,url_prefix = '/')

@page_bp.route('/')
@login_required
def 首页():
    return render_template('index.html')

@page_bp.route('/query',methods = ['GET','POST'])
@login_required
def 查询():
    if request.method == 'POST':
        批号 = request.form['批号']
        数据 = dt.读取所有数据()
        for i in 数据:
            if i[0] == 批号:
                return f'批号：{i[0]}，收率：{i[1]}，结果：{i[2]}，日期：{i[3]}'
            else:
                return redirect(url_for('page.message',message = f'无批号：{批号}数据!'))
    return render_template('/query.html')

@page_bp.route('new',methods = ['GET','POST'])
@login_required
def 追加记录():
    if request.method == 'POST':
        批号 = request.form['批号']
        收率 = float(request.form['收率'])
        日期_str = request.form['日期']
        日期 = datetime.strptime(日期_str,'%Y-%m-%d')
        结果 = sv.结果判断(收率)
        user_id = current_user.id
        dt.追加记录(批号,收率,结果,日期,user_id)
        return redirect(url_for('page.message',message = '该批号已保存！'))
    return render_template('/new.html')
    
@page_bp.route('all',methods = ['GET'])
@login_required
def 所有数据():
    if current_user.role == 'admin':
        数据 = dt.执行查询('SELECT * FROM 批记录')
    else:
        user_id = current_user.id
        数据 = dt.执行查询('SELECT * FROM 批记录 WHERE user_id = %s',(user_id,))
    return render_template('/all.html',数据 = 数据)

@page_bp.route('stat',methods = ['GET','POST'])
@login_required
def 统计():
    if current_user.role == 'admin':
        数据 = dt.读取所有数据()
        总批数,合格批数,合格率 = sv.统计合格率(数据)
        return render_template('/stat.html',总批数 = 总批数,合格批数 = 合格批数,合格率 = 合格率)
    else:
        return redirect(url_for('page.message',message = '暂无权限查看记录！'))

@page_bp.route('user_inf',methods = ['GET'])
@login_required
def user_inf():
    username = current_user.username
    当前用户信息 = dt.执行查询('SELECT * FROM users WHERE username = %s',(username,))
    return render_template('user_inf.html',当前用户信息=当前用户信息)

@page_bp.route('message/<message>',methods = ['GET'])
@login_required
def message(message = None):
    return render_template('/message.html',message = message)

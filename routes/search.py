from flask import Blueprint,render_template,request
import data as dt
import service as sv
from datetime import datetime

search_bp = Blueprint('search',__name__,url_prefix = '/')

@search_bp.route('/search_by_date',methods = ['GET','POST'])
def 按日期搜索():
    if request.method == 'POST':
        目标日期_str=request.form['目标日期']
        if 目标日期_str is None:
            return f'请输入日期！'
        目标日期 = datetime.strptime(目标日期_str,'%Y-%m-%d').date()
        数据 = dt.读取所有数据()
        结果 = []
        for i in 数据:
            if i[3] >= 目标日期:
                结果.append(i)
        return render_template('/search_by_date_result.html',数据=结果,日期 = 目标日期)
    return render_template('/search_by_date.html')

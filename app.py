from flask import Flask,render_template,request
from datetime import datetime
import data as dt
import service as sv
app=Flask(__name__)
@app.route("/")
def 首页():
    return render_template('index.html')
@app.route("/query",methods=['POST','GET'])
def 查询():
    if request.method=="POST":
        批号=request.form['批号']
        结果=dt.查找批号(批号)
        if 结果:
            return f'批号：{结果[0]}，收率：{结果[1]}，结果：{结果[2]},日期：{结果[3]}'
        else:
            return '未找到该批号'
    return render_template('query.html')
@app.route("/all",methods=['POST','GET'])
def 所有记录():
    if request.method == 'GET':
        数据=dt.读取所有数据()
    return render_template("all.html",数据=数据)
@app.route('/new',methods=['POST','GET'])
def 录入():
    if request.method=='POST':
        批号 = request.form['批号']
        收率 = float(request.form['收率'])
        结果=sv.结果判断(收率)
        日期 = request.form['日期']
        dt.追加记录(批号,收率,结果,日期)
        return f'批号：{批号}已保存，结果：{结果}'
    return render_template("new.html")
@app.route('/stat',methods=['GET','POST'])
def 统计():
    数据=dt.读取所有数据()
    总批数,合格批数,合格率=sv.统计合格率(数据)
    return render_template('stat.html',总批数=总批数,合格批数=合格批数,合格率=合格率)

@app.route('/search_by_date',methods = ["GET","POST"])
def 按照日期查询():
    if request.method == 'POST':
        目标日期 = datetime.strptime(request.form['目标日期'],'%Y-%m-%d').date()
        数据 = dt.读取所有数据()
        结果 = []
        for i in 数据:
            if i[3] >= 目标日期:
                结果.append(i)
        return render_template('search_by_date_result.html',数据=结果,日期=目标日期)
    return render_template('search_by_date.html')
if __name__ =='__main__':
    app.run(debug=True)

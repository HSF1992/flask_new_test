from flask import Flask,render_template,request
import data as dt
import service as sv
app=Flask(__name__)
@app.route("/")
def 首页():
    return render_template('index.html')
@app.route("/query",methods=['post','get'])
def 查询(批号):
    if request.method=="post":
        批号=request.form['批号']
        结果=sv.查找批号(批号)
        if 结果:
            return f'批号：{结果[0]}，收率：{结果[1]}，结果：{结果[2]}'
        else:
            return '未找到该批号'
        return render_template('/query.html')
@app.route("/all",methods=['post','get'])
def 所有记录():
    数据=dt.读取所有数据()
    return render_template("/all.html")
@app.route('/new',methods=['post','get'])
def 录入():
    if request.method=='post':
        批号=request.form['批号']
        收率=float(request.form['收率'])
        结果=sv.结果判断(批号)
        return f'批号：{批号}已保存，结果：{结果}'
    return render_template("/new.html")
@app.route('/stat',methods=['get','post'])
def 统计():
    数据=dt.读取所有数据()
    总批数,合格批数,合格率=sv.统计合格率(数据)
    return render_template('/stat.html',总批数=总批数,合格批数=合格批数,合格率=合格率)
if __name__=='__main__':
    app.run(debug=True)


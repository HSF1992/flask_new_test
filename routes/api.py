from flask import Blueprint, jsonify, request
import data as dt
import service as sv

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/records', methods=['GET'])
def 获取所有记录():
    数据 = dt.读取所有记录()
    return jsonify(数据)

@api_bp.route('record/<batch_no>', methods=['GET'])
def 按批号查询(batch_no):
    数据 = dt.读取所有记录()
    for 行 in 数据:
        if 行[0] == batch_no:
            return jsonify(行)
    return jsonify({"错误": "未找到该批号"}), 404

@api_bp.route('/record', methods=['POST'])
def 新增记录():
    数据 = request.get_json()
    批号 = 数据.get('批号')
    收率 = 数据.get('收率')
    日期 = 数据.get('日期')
    if not 批号 or 收率 is None:
        return jsonify({"错误": "缺少批号或收率"}), 400
    if 日期 is None:
        from datetime import datetime
        日期 = datetime.now().date().strptime('%Y-%m-%d')
    结果 = sv.判断收率是否合格(收率)
    dt.追加记录(批号,收率,结果,日期)
    return jsonify({"消息": "保存成功", "结果": 结果}), 201

@api_bp.route('/stat', methods=['GET'])
def 统计():
    数据 = dt.读取所有记录()
    总批数, 合格批数, 合格率 = sv.统计合格率(数据)
    return jsonify({
        "总批数": 总批数,
        "合格批数": 合格批数,
        "合格率": 合格率
    })

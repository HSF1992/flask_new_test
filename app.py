from flask import Flask
from flask_login import LoginManager
from routes.page import page_bp
from routes.api import api_bp
from routes.search import search_bp
from routes.auth import auth_bp,user
import data as dt

app=Flask(__name__)
app.secret_key = "Hsf110612"
app.config['session_permanent'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

app.register_blueprint(page_bp)
app.register_blueprint(api_bp)
app.register_blueprint(search_bp)
app.register_blueprint(auth_bp)

@login_manager.user_loader
def load_user(user_id):
    用户数据 = dt.执行查询("SELECT * FROM users WHERE id = %s",(user_id,))
    if 用户数据:
        return user(用户数据[0][0],用户数据[0][1],用户数据[0][3])
    return None

if __name__ =='__main__':
    app.run(debug=True)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
#加载配置文件
app.config.from_object('config')
db = SQLAlchemy(app)
   
from app import views,models

#声明login对象 并初始化app
login_manager = LoginManager()
login_manager.init_app(app)

#未登录会跳转到login
login_manager.login_view = "login"

#当登陆成功后，该函数会自动从会话中存储的用户 ID 重新加载用户对象。
#它接受一个用户的 unicode ID 作为参数，并且返回相应的用户对象。
@login_manager.user_loader
def load_user(id):
    return models.User.query.get(int(id))
    
from app import admin

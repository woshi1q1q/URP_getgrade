from flask_admin import Admin,BaseView,expose,AdminIndexView
from flask_admin.contrib.sqla import ModelView
from app import app,db
from app.models import User,Post,Comment
from flask_login import current_user

admin = Admin(app,name='管理页面',index_view=AdminIndexView(
        name='导航栏'))

class MyView(ModelView):
    #处于登录状态并且为admin用户的时候，才能进行相关显示以及操作
    def is_accessible(self):
            if current_user.is_authenticated and current_user.username == "admin":
                return True
            return False
    can_create = False
    
admin.add_view(MyView(User,db.session, name = '用户管理'))
admin.add_view(MyView(Post,db.session, name = '文章管理'))
admin.add_view(MyView(Comment,db.session, name = '评论管理'))
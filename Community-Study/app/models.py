from app import db
from datetime import datetime
from flask_login import UserMixin
import bleach
from markdown import markdown

class User(db.Model,UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    email = db.Column(db.String(50))
    author = db.relationship('Post',backref='author',lazy='dynamic')
    
    
    def __str__(self):
                return self.username
    
    __repr__=__str__

class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer,primary_key=True)    
    create_time = db.Column(db.DateTime,default=datetime.now)
    title = db.Column(db.String(70))
    post = db.Column(db.Text)
    author_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    body_html=db.Column(db.Text)
    
    #处理body字段变化的函数
    @staticmethod
    def on_changed_post(target,value,oldvalue,initiaor):
        allow_tags=['a','abbr','acronym','b','blockquote','code',
                    'em','i','li','ol','pre','strong','ul',
                    'h1','h2','h3','p','img']
        #转换markdown为html，并清洗html标签
        target.body_html=bleach.linkify(bleach.clean(
            markdown(value,output_form='html'),
            tags=allow_tags,strip=True,
            attributes={
                '*': ['class'],
                'a': ['href', 'rel'],
                'img': ['src', 'alt'],#支持<img src …>标签和属性
            }
    ))
    
    def __str__(self):
                return self.title
    __repr__=__str__ 


#注册监听事件
db.event.listen(Post.post,'set',Post.on_changed_post)
    
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key=True)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime,default=datetime.now)
    name_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    name = db.relationship('User',backref=db.backref('comments',lazy='dynamic')) 
    post_id = db.Column(db.Integer)
    body_html=db.Column(db.Text)
    
    #处理body字段变化的函数
    @staticmethod
    def on_changed_comment(target,value,oldvalue,initiaor):
        allow_tags=['a','abbr','acronym','b','blockquote','code',
                    'em','i','li','ol','pre','strong','ul',
                    'h1','h2','h3','p','img']
        #转换markdown为html，并清洗html标签
        target.body_html=bleach.linkify(bleach.clean(
            markdown(value,output_form='html'),
            tags=allow_tags,strip=True,
            attributes={
                '*': ['class'],
                'a': ['href', 'rel'],
                'img': ['src', 'alt'],#支持<img src …>标签和属性
            }
    ))
    def __str__(self):
                return self.content 
    __repr__=__str__
db.event.listen(Comment.content,'set',Comment.on_changed_comment)

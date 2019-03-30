from app import app,db
from flask import request,render_template,redirect,url_for,flash,Response
from app.models import User,Post,Comment
from flask_login import login_required, login_user, logout_user,current_user
import os
from datetime import datetime
from flask import jsonify

@app.route('/',methods=['GET','POST'])
@app.route('/page/<int:page>/',methods=['GET','POST'])
def home(page=1):
    posts = Post.query.order_by(-Post.create_time).paginate(page,10,False)
    post_list = Post.query.order_by(-Post.create_time).all()
    if request.method == 'POST':
        return redirect(url_for('home',page=request.form['page_num']))
    return render_template('home.html',post_list=post_list,posts=posts)




@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter(User.username==request.form['username'],User.password==request.form['password']).first()
        if user != None:
            login_user(user)
            flash('登录成功！')
            return redirect(url_for('home'))
        else:
            flash('账号或密码有误！')    
    return render_template('login.html')

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('你已成功退出！')
    return redirect(url_for('home'))
    
@app.route('/reg/',methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if name=='' or password=='':
            flash('用户名或密码为空')
        else:
            user = User.query.filter(User.username==name).first()
            if user == None:
                newuser = User(username=name,password=password,email=email)
                db.session.add(newuser)
                db.session.commit()
                flash('注册成功，请登录！')
                return redirect(url_for('login'))
            else:
                flash('用户名已存在！')  
    return render_template('reg.html')
  
@app.route('/new/',methods=['GET','POST'])
@login_required 
def newpost():
    post_list = Post.query.order_by(-Post.create_time).all()
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        newpost = Post(title=title,post=content,author=current_user)
        db.session.add(newpost)
        db.session.commit()
        flash('发布成功！')
        return redirect(url_for('home'))
    return render_template('new.html',post_list=post_list)
    
@app.route('/detail/<int:id>/',methods=['GET','POST'])
def detail(id):
    detail = Post.query.get_or_404(id)
    post_list = Post.query.order_by(-Post.create_time).all()
    comment_list = Comment.query.filter(Comment.post_id==id).order_by(-Comment.create_time).all()
    if request.method == "POST":
        content = request.form['content']
        new_comment = Comment(content=content,name=current_user,post_id=id)
        db.session.add(new_comment)
        db.session.commit()
        flash('评论成功！')
        return redirect(url_for('detail',id=id))
    return render_template('detail.html',post_list=post_list,detail=detail,comment_list=comment_list)

@app.route('/mypage/')
@login_required
def mypage():
    post_list = Post.query.order_by(-Post.create_time).all()
    user = User.query.filter(User.username==str(current_user)).first()
    my_posts = Post.query.filter(Post.author==current_user).order_by(-Post.create_time).all()
    return render_template('mypage.html',post_list=post_list,user=user,my_posts=my_posts)
  
@app.route('/about/')
def about():
    return render_template('about.html')
    
@app.route('/delete/info/<int:id>/')   
@login_required
def delete_post_info(id):
    post_list = Post.query.order_by(-Post.create_time).all()
    data = Post.query.filter(Post.id==id).first()
    return render_template('delete_info.html',post_list=post_list,data=data)
    
@app.route('/delete/<int:id>/')   
@login_required
def delete_post(id):    
    data = Post.query.filter(Post.id==id).first()
    if current_user == data.author:
        db.session.delete(data)
        db.session.commit()
        flash('删除成功！')        
    else:
        flash('删除失败！')
        flash('原因:身份验证不成功！')
    return redirect(url_for('mypage'))
    
@app.route('/edit/<int:id>/',methods=['GET','POST'])
@login_required
def edit_post(id):
    post_list = Post.query.order_by(-Post.create_time).all()
    data = Post.query.filter(Post.id==id).first()
    if data != None and current_user == data.author:
        if request.method == 'POST':
            title = request.form['title']
            post = request.form['content']
            data.title = title
            data.post = post
            db.session.commit()
            flash('修改成功！')
            return redirect('mypage')
        return render_template('edit_post.html',post_list=post_list,data=data)      
    else:
        flash('请求参数有误！')
        return redirect(url_for('mypage'))
             
# 图片上传处理
@app.route('/upload/',methods=['POST'])
def upload():
    file=request.files.get('editormd-image-file')
    basedir = os.path.abspath(os.path.dirname(__file__))
    if not file:
        res={
            'success':0,
            'message':u'图片格式异常'
        }
    else:
        path = basedir+'/static/uploads/'
        ex=os.path.splitext(file.filename)[1]
        filename=datetime.now().strftime('%Y%m%d%H%M%S')+ex
        file.save(path+filename)
        #返回
        res={
            'success':1,
            'message':u'图片上传成功',
            'url':url_for('image',name=filename)
        }
    return jsonify(res)

#编辑器上传图片处理
@app.route('/image/<name>')
def image(name):
    with open(os.path.join(os.path.abspath('.')+'/app/static/uploads',name),'rb') as f:
        resp=Response(f.read(),mimetype="image/jpeg")
    return resp

from flask import Flask,render_template,request,redirect,url_for,session,g
import config
from models import User,Question,Answer
from exts import db
from decorators import login_required
from sqlalchemy import or_
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
@app.route('/')
def index():
    context={
        'questions':Question.query.order_by('-create_time').all()
    }
    return render_template('index.html',**context)

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone =request.form.get('telephone')
        password = request.form.get('password')
        #校验用户是否存在
        # user = User.query.filter(User.telephone == telephone,User.password == password).first()
        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_passwd(password):
            session['user_id'] = user.id
            #开启31天免密码登录
            session.permanent = True
            return  redirect(url_for('index'))
        else:
            return '手机号码或者密码错误'


@app.route('/regist/',methods=['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('usename')
        password1 = request.form.get('passwd1')
        password2 = request.form.get('passwd2')
        #手机号码验证，如果注册就不能再次注册
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return '该手机号码已经注册，请换一个手机号码'
        else:
            #passwd1与passwd2是否相等
            if password1 != password2:
                return '两次输入的号码不想等'
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                #如果注册成功，就让页面跳转至登录页面
                return redirect(url_for('login'))

@app.route('/logout/')
def logout():
    #session.pop('user_id')
    del session['user_id']
    return redirect(url_for('login'))

@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return  render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        # user_id = session.get('user_id')
        # user = User.query.filter(User.id == user_id).first()
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))
@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html',question = question_model)

@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')
    answer = Answer(content = content )
    # user_id = session['user_id']
    # user = User.query.filter(User.id == user_id).first()
    answer.author = g.user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))

@app.route('/serch/')
def serch():
    q = request.args.get('q')
    #title content
    #如果用户没有传入任何参数时，请查询是请展示所有内容
    if q == "":
        context = {
            'questions': Question.query.order_by('-create_time').all()
        }
        return render_template('index.html', **context)
    else:
        questions = Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q))).order_by('-create_time')
        return render_template('index.html',questions=questions)
#上下文管理器
@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user

@app.context_processor
def my_context_processor():
    # user_id = session.get('user_id')
    # if user_id:
    #     user = User.query.filter(User.id == user_id).first()
    #     if user:
    #         return {'user':user}
    # else:
    #     return {}
    #使用全局G对象，如果g里面含有user,则直接返回user
    if hasattr(g,'user'):
        return {'user':g.user}
    return {}

if __name__ == '__main__':
    app.run()

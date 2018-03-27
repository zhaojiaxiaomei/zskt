from flask import Flask,render_template,request,redirect,url_for,session,g
from models import User,Question,Answer
from exts import db
import config
from decorators import login_required
from sqlalchemy import or_

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

'''
首页
'''
@app.route('/')
def index():
    questions = Question.query.order_by('-create_time').all()
    content = {
        'questions':questions
    }
    return render_template('index.html',questions = questions)

'''
登录
'''
@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            if user.check_password(password):
                session['user_id'] = user.id
                session.permanent = True
                return redirect(url_for('index'))
            else:
                return '用户名或密码错误'
        else:
            return '您还没有注册'


'''
注册
'''
@app.route('/regist/',methods = ['GET','POST'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return '该用于已经注册'
        else:
            if password1 != password2:
                return '两次输入的密码不一致'
            else:
                user = User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/question/',methods = ['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        question.author = g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}

@app.route('/detail/<question_id>')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question = question_model)

@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    question_id = request.form.get('question_id')
    question_model = Question.query.filter(Question.id == question_id).first()
    content = request.form.get('answer_content')
    answer= Answer(content=content)
    answer.question=question_model
    answer.author=g.user
    db.session.add(answer)
    db.session.commit()
    #return redirect(url_for('detail',question_id=question_id))
    return render_template('detail.html', question=question_model)

@app.route('/serach_q/')
def serach_q():
    q = request.args.get('q')
    questions = Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q)))
    return render_template('index.html',questions=questions)

@app.route('/logout/')
def logout():
    del session['user_id']
    return redirect(url_for('login'))

@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        g.user=user

if __name__ == '__main__':
    app.run()

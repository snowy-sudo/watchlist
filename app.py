from flask import Flask,render_template
# app = Flask(__name__)
# @app.route('/')
# def hello():
#     return '<h1>我将畅游!</h1><img src="https://assets.699pic.com/public/img95/photo/40130/5797.gif_wh860.gif">'

# @app.route('/user/<name>')
# def user_page(name):
#     return f'User {name} page '



# #视图函数
# from markupsafe import escape
# @app.route('/user/<name>')
# def user_page(name):
#     return f'User {escape(name)} '


from flask import url_for
from markupsafe import escape
#...
# @app.route('/')
# def hello():
#     return 'Hello'

# @app.route('/user/<name>')
# def user_page(name):
#     return f'User:{escape(name)}'

# @app.route('/test')
# def test_url_for():
#     #下面是一些调用示例（访问http://localhost:5000/test 后在命令行窗口看输出的URL）：
#     print(url_for('hello'))  #生成hello 视图函数对应的URL，将会输出：/
#     print(url_for('user_page',name='snowy-sudo'))  #输出/user/snowy-sudo
#     print(url_for('test_url_for'))  #输出：/test
#     #下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到URL后面
#     print(url_for('test_url_for',num=2))  #输出：/test?num=2
#     return 'Test page'

#定义虚拟数据
# name = 'Snowy-sudo'
# movies = [
#     {'title': 'My Neighbor Totoro', 'year': '1988'},
#     {'title': 'Dead Poets Society', 'year': '1989'},
#     {'title': 'A Perfect World', 'year': '1993'},
#     {'title': 'Leon', 'year': '1994'},
#     {'title': 'Mahjong', 'year': '1996'},
#     {'title': 'Swallowtail Butterfly', 'year': '1996'},
#     {'title': 'King of Comedy', 'year': '1999'},
#     {'title': 'Devils on the Doorstep', 'year': '1999'},
#     {'title': 'WALL-E', 'year': '2008'},
#     {'title': 'The Pork of Music', 'year': '2012'},
# ]
# @app.route('/')
# def index():
#     return render_template('index.html',name=name,movies=movies)


""" 连接数据库"""
from pathlib import Path
from sqlalchemy import String
from flask_sqlalchemy import SQLAlchemy   #导入扩展类
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column



#1.先定义Base、先创建对象db对象（不要传app!）
class Base(DeclarativeBase):
    pass
#db = SQLAlchemy(app,model_class=Base)  #初始化扩展，传入程序实例app
db = SQLAlchemy(model_class=Base) 
app = Flask(__name__)
#数据库配置
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + str(Path(app.root_path) / 'data.db').lstrip('/')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#2.再init_app挂载app
db.init_app(app)

#模型放这里
class User(db.Model):
    __tablename__ = 'user' # 定义表名称
    id: Mapped[int] = mapped_column(primary_key=True)  # 主键
    name: Mapped[str] = mapped_column(String(20))  # 名字
class Movie(db.Model):  # 表名将会是 movie
    __tablename__ = 'movie'
    id: Mapped[int] = mapped_column(primary_key=True)  # 主键
    title: Mapped[str] = mapped_column(String(60))  # 电影标题
    year: Mapped[str] = mapped_column(String(4))  # 电影年份


#===============自定义init-db命令（修复上下文问题）=============
#自定义命令创建数据库表操作
# import click
# @app.cli.command('init-db') #注册为命令。传入自定义命令
# @click.option('--drop',is_flag=True,help='Create after drop.') #设置选项
# def init_database(drop):
#     """Initialize the database."""
#     if drop: #判断是否输入了选项
#         db.drop_all()
#     db.create_all()
#     click.echo('Initialized database.') #输出提示信息

#=================在主页视图读取数据库记录=============
from sqlalchemy import select,func
@app.route('/')
def index():
    user = db.session.execute(select(User)).scalar()  #读取用户记录
    movies = db.session.execute(select(Movie)).scalars().all()  #读取所有电影记录
    return render_template('index.html',user=user,movies=movies)

#===============创建自定义命令forge===============

import click

@app.cli.command()
def forge():
    """Generate fake data."""
    db.drop_all()
    db.create_all()

    #全局的两个变量移动到这个函数内
    name = 'Snowy-sudo'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie =Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('Done.')
 
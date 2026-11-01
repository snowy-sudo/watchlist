from flask import Flask
app = Flask(__name__)
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
@app.route('/')
def hello():
    return 'Hello'

@app.route('/user/<name>')
def user_page(name):
    return f'User:{escape(name)}'

@app.route('/test')
def test_url_for():
    #下面是一些调用示例（访问http://localhost:5000/test 后在命令行窗口看输出的URL）：
    print(url_for('hello'))  #生成hello 视图函数对应的URL，将会输出：/
    print(url_for('user_page',name='snowy-sudo'))  #输出/user/snowy-sudo
    print(url_for('test_url_for'))  #输出：/test
    #下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到URL后面
    print(url_for('test_url_for',num=2))  #输出：/test?num=2
    return 'Test page'